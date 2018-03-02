import json

from django.db import models, connection
from rest_framework import exceptions


def recordset(raw):

    sql = '''select * from json_to_recordset({})
             as x(id int, income int, veteran bool)''' \
          .format(json.dumps(raw))

    import pytest; pytest.set_trace()
    with connection.cursor() as cursor:
        connection.execute(sql)
        for row in cursor.fetchall():
            print(row)


class Ruleset(models.Model):
    program = models.TextField(null=False, blank=False)
    entity = models.TextField(null=False, blank=False)

    def apply_to(self, applicants):
        for applicant in applicants:
            try:
                id = applicant['id']
                result = {'id': id, 'accepted': False, 'reasons': [{'rule_id': 1, 'description': 'Just because'}]}
                yield result
            except KeyError:
                reason = 'Applicant lacks "id" field: {}'.format(applicant)
                raise exceptions.ValidationError(reason)


    # TODO: keep old rulesets when rules change?

class Rule(models.Model):
    order = models.IntegerField(null=False, blank=False)
    name = models.TextField(null=False, blank=False)
    code = models.TextField(null=False, blank=False)
    explanation = models.TextField(null=False, blank=False)
    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE)

    # TODO: Parameterization, for similar rules with simple differences
