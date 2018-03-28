from copy import deepcopy

from django.contrib.postgres.fields.jsonb import JSONField
from django.db import connection, models
from prettytable import from_db_cursor

from .utils import values_from_json


class Ruleset(models.Model):
    program = models.TextField(null=False, blank=False)
    entity = models.TextField(null=False, blank=False)
    sample_input = JSONField(null=True, blank=True)
    null_sources = JSONField(null=True, blank=True)

    @property
    def schema(self):
        return self.syntaxschema_set.first()

    def flattened(self, payload):
        applicants = payload.pop('applicants')
        for applicant in applicants:
            applicant_info = deepcopy(payload)
            applicant_info.update(applicant)
            yield applicant_info

    def null_source_sql(self, raw):
        for (key, val) in self.null_sources.items():
            if key not in raw:
                yield " %s as ( select * from %s ) " % (key, val)

    def source_sql_statements(self, raw):
        with connection.cursor() as cursor:
            for (source_sql, source_data) in values_from_json(
                    raw, self.schema):
                table_name = source_sql.split()[0]
                source_sql = "with " + source_sql + " select * from " + table_name
                source_sql = source_sql.replace("%s", "'%s'") % source_data
                yield (source_sql)
                cursor.execute(source_sql)
                yield str(from_db_cursor(cursor))

    def values_from_json(self, raw):

        (source_sql,
         source_data) = zip(*(values_from_json(raw, schema=self.schema)))
        source_sql += tuple(self.null_source_sql(raw))
        source_clause = 'WITH ' + ',\n'.join(source_sql)
        return (source_clause, source_data)

    def calc(self, application):

        overall_result = {}
        for applicant in self.flattened(application):
            eligibility = True
            result = {'requirements': {}}
            (source_clause, source_data) = self.values_from_json(applicant)
            for node in self.node_set.all():
                node_result = node.calc(source_clause, source_data)
                result['requirements'][node.name] = node_result
                if node.name != 'categories':
                    eligibility &= node_result['eligible']
            result['eligible'] = eligibility
            overall_result[int(applicant['id'])] = result

            categories = result['requirements'].pop('categories')
            category_names = [
                key for (key, val) in categories['subfindings'].items()
                if val['eligible']
            ]
            result['categories'] = {
                'applicable': category_names,
                'findings': categories['subfindings']
            }

            overall_result[int(applicant['id'])] = result
        return overall_result

    def sql(self, application):

        for applicant in self.flattened(application):
            (source_clause, source_data) = self.values_from_json(applicant)
            for node in self.node_set.all():
                yield from node.sql(source_clause, source_data)


class Node(models.Model):
    name = models.TextField(null=False, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    ruleset = models.ForeignKey(Ruleset, null=True, on_delete=models.CASCADE)
    requires_all = models.BooleanField(null=False, blank=False, default=False)

    @property
    def get_ruleset(self):
        return self.ruleset or self.parent.get_ruleset

    def sql(self, source_clause, source_data):
        for rule in self.rule_set.all():
            yield rule.sql(source_clause, source_data)

    def calc(self, source_clause, source_data):

        if self.requires_all:
            eligibility = True
        else:
            eligibility = False

        node_result = {'limitation': [], 'explanation': [], 'subfindings': {}}

        for child_node in self.node_set.all():
            child_node_result = child_node.calc(source_clause, source_data)
            # todo : well, now what?

        for rule in self.rule_set.all():
            rule_result = rule.calc(source_clause, source_data)
            node_result['explanation'].append(rule_result['explanation'])
            if self.requires_all:
                eligibility &= rule_result['eligible']
            else:
                eligibility |= rule_result['eligible']
            if rule_result['eligible']:
                node_result['limitation'].append(rule_result['limitation'])
            node_result['subfindings'][rule.name] = rule_result

        if self.rule_set.count() == 1:
            node_result.pop('subfindings')

        node_result['eligible'] = eligibility
        return node_result


class Rule(models.Model):
    name = models.TextField(null=False, blank=False)
    code = models.TextField(null=True, blank=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    sufficient = models.BooleanField(null=False, blank=False, default=False)

    @property
    def ruleset(self):
        return self.node.get_ruleset

    _SQL = """with source as (%s %s)
              select (source.result).eligible,
                     (source.result).explanation,
                     ((source.result).limitation).end_date,
                     ((source.result).limitation).normal,
                     ((source.result).limitation).description,
                     ((source.result).limitation).explanation AS limitation_explanation
              from source"""

    def calc(self, source_clause, source_data):

        with connection.cursor() as cursor:
            sql = self._SQL % (source_clause, self.code)
            cursor.execute(sql, tuple(source_data))
            findings = cursor.fetchone()
        limitation = dict(
            zip(('end_date', 'normal', 'description', 'explanation'),
                findings[2:]))
        return {
            'eligible': findings[0],
            'explanation': findings[1],
            'limitation': limitation
        }

    def sql(self, source_clause, source_data):
        result = self._SQL % (source_clause, self.code)
        result = result.replace("%s", "'%s'")
        return result % source_data


class SyntaxSchema(models.Model):
    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE)
    type = models.TextField(null=False, blank=False, default='jsonschema')
    code = JSONField(null=False, blank=False)

    def walk(self, node=None):
        """Yields all the dictionaries in a nested structure."""

        node = node or self.code

        if isinstance(node, list):
            for itm in node:
                yield from self.walk(itm)
        else:
            yield node
            for (key, val) in node.items():
                if isinstance(val, dict):
                    yield from self.walk(val)

    _JSONSCHEMA_TO_PG_TYPES = {
        'integer': 'integer',
        'number': 'numeric',
        'string': 'text',
        'date': 'date',
        'boolean': 'boolean',
    }

    def _col_data_type(self, col_data):
        if col_data.get('format') == 'date-time':
            return 'date'
        elif col_data.get('$ref') == '#/definitions/ynexception':
            return 'text'
        else:
            data_type = col_data.get('type', 'text')
            if isinstance(data_type, list):
                data_type = [dt for dt in data_type if dt != 'null']
                if len(data_type) > 1:
                    data_type = 'text'
                else:
                    data_type = data_type[0]
            return self._JSONSCHEMA_TO_PG_TYPES.get(data_type)

    def data_types(self):
        result = {}
        for node in self.walk():
            for (col_name, col_data) in node.get('properties', {}).items():
                col_type_from_schema = self._col_data_type(col_data)
                if col_type_from_schema:
                    result[col_name] = self._col_data_type(col_data)
        return result

    # todo: this should be one-to-one, or sorted so that the
    # type-determiner comesfirst?
