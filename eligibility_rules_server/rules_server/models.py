import json

import sqlparse
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import connection, models
from prettytable import from_db_cursor

from .utils import all_values_from_json, values_from_json


class Ruleset(models.Model):
    program = models.TextField(null=False, blank=False)
    entity = models.TextField(null=False, blank=False)
    summarizer = models.TextField(null=False, blank=False)
    sample_input = models.TextField(null=True, blank=True)

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

    _COLUMNS = ('applicant_id', 'qualifies', 'limitations', 'findings')

    def assess(self, payload):

        (sql, source_data) = self.sql_form(payload)

        with connection.cursor() as cursor:
            cursor.execute(sql, tuple(source_data))
            result = [dict(zip(self._COLUMNS, row)) for row in cursor]
        return result


class Rule(models.Model):
    name = models.TextField(null=False, blank=False)
    code = models.TextField(null=False, blank=False)
    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE)

    def sql(self, source_sql):
        """
        Must return an (applicants_id, findings::finding)
        """

        return """%s_source AS (
        %s
        %s
        )
        """ % (self.name, source_sql, self.code)


class SyntaxSchema(models.Model):
    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE)
    type = models.TextField(null=False, blank=False, default='jsonschema')
    code = JSONField(null=False, blank=False)
