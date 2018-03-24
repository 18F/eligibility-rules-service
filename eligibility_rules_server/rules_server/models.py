import json
from copy import deepcopy

import sqlparse
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import connection, models
from prettytable import from_db_cursor

from .utils import values_from_json


class Ruleset(models.Model):
    program = models.TextField(null=False, blank=False)
    entity = models.TextField(null=False, blank=False)
    sample_input = models.TextField(null=True, blank=True)
    null_sources = JSONField(null=True, blank=True)

    def flattened(self, payload):
        applicants = payload.pop('applicants')
        for (applicant_id, applicant) in applicants.items():
            applicant_info = deepcopy(payload)
            applicant_info.update(applicant)
            # for (key, value) in self.applicant_zero_info.items():
            #     if (key not in applicant_info):
            #         applicant_info[key] = value
            yield (applicant_id, applicant_info)

    def null_source_sql(self, raw):
        for (key, val) in self.null_sources.items():
            if key not in raw:
                yield " %s as ( select * from %s ) " % (key, val)

    def values_from_json(self, raw):
        (source_sql, source_data) = zip(*(values_from_json(raw)))
        source_sql += tuple(self.null_source_sql(raw))
        source_clause = 'WITH ' + ',\n'.join(source_sql)
        return (source_clause, source_data)

    def calc(self, application):

        overall_result = {}
        for (applicant_id, applicant) in self.flattened(application):
            eligibility = True
            result = {'requirements': {}}
            (source_clause, source_data) = self.values_from_json(applicant)
            for node in self.node_set.all():
                node_result = node.calc(source_clause, source_data)
                result['requirements'][node.name] = node_result
                eligibility &= node_result['eligible']
            result['eligible'] = eligibility
            overall_result[int(applicant_id)] = result
        return overall_result

    def sql_form(self, payload=None):
        if payload is None:
            payload = json.loads(self.sample_input) or []
        (source_clause, source_data) = all_values_from_json(payload)
        sql = ("with " + "\n, ".join(
            r.sql(source_clause) for r in self.rule_set.order_by('id')) +
               self.summarizer + ' order by 1')
        return (sql, source_data * self.rule_set.count())

    def sql_form_report(self, payload=None):

        result = []
        with connection.cursor() as cursor:
            for (sql, source_data) in values_from_json(payload):
                executable = sql % ("'%s'" % source_data)
                result.append(executable)
                executable = '\n'.join(
                    executable.splitlines()[1:])  # drop first line
                try:
                    cursor.execute(executable)
                except Exception as e:
                    result = str(e) + '\n\n\n' + sqlparse.format(executable)
                    return result
                result.append(from_db_cursor(cursor).get_string())

        (sql, source_data) = self.sql_form(payload)
        sql = sql.replace("(%s)", "('%s')")
        result.append(sqlparse.format(sql % source_data))
        return '\n\n\n'.join(result)

    _COLUMNS = ('applicant_id', 'eligible', 'limitations', 'findings')

    def assess(self, payload):

        (sql, source_data) = self.sql_form(payload)

        with connection.cursor() as cursor:
            cursor.execute(sql, tuple(source_data))
            result = [dict(zip(self._COLUMNS, row)) for row in cursor]
        return result


class Node(models.Model):
    name = models.TextField(null=False, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    ruleset = models.ForeignKey(Ruleset, null=True, on_delete=models.CASCADE)
    requires_all = models.BooleanField(null=False, blank=False, default=False)

    @property
    def get_ruleset(self):
        return self.ruleset or self.parent.get_ruleset

    def calc(self, source_clause, source_data):

        if self.requires_all:
            eligibility = True
        else:
            eligibility = False

        node_result = {'limitation': [], 'explanation': [], 'subfindings': {}}

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

    def calc(self, source_clause, source_data):

        with connection.cursor() as cursor:
            sql = """with source as (%s %s) select (source.result).eligible, (source.result).limitation, (source.result).explanation
            from source""" % (source_clause, self.code)
            cursor.execute(sql, tuple(source_data))
            findings = cursor.fetchone()
        return dict(zip(('eligible', 'limitation', 'explanation'), findings))

    def sql(self, source_sql):
        """
        Must return an (applicants_id, findings::finding)
        """

        return """%s_source AS (
        %s
        %s
        )
        """ % (self.name, source_sql, self.code)

    def result(self, payload):
        (source_clause, source_data) = all_values_from_json(payload)
        source_clause + self.code, source_data
        response = {}
        with connection.cursor() as cursor:
            cursor.execute(source_clause + self.code, tuple(source_data))
        return cursor.fetchone()


class SyntaxSchema(models.Model):
    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE)
    type = models.TextField(null=False, blank=False, default='jsonschema')
    code = JSONField(null=False, blank=False)
