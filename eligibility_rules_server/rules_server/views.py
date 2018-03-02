from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

from .models import Ruleset


class RulingsView(APIView):
    """
    Returns a series of findings, one per applicant

    The rule set applied to the findings is determined by the
    program and entity from the URL.

    Applicant data should be included in the payload.  The fields
    included may vary by program and state, but the minimum
    required for every payload is:

        {
          "applicants": [
            {
              "id": 1,
              ... (other applicant data)
            },
            {
              "id": 2
              ... (other applicant data)
            },
            ...
          ]
        }

    `id` need not be numeric, but must be unique per applicant.
    It is only used to match findings to applicants.

    Response will be in the form

        {
          "findings": [
            {
              "id": 1,
              "reasons": [],
              "accepted": true
            },
            {
              "reasons": [
                {
                  "description": "Too cool for school",
                  "rule_id": 101
                },
                {
                  "description": "Can't touch this",
                  "rule_id": 103
                }
              ],
              "accepted": false
            }
          ]
        }

    """

    def post(self, request, program, entity, format=None):

        try:
            ruleset = Ruleset.objects.get(program=program, entity=entity)
        except Ruleset.DoesNotExist:
            detail = "Ruleset for program '{}', entity '{}' has not been defined".format(program, entity)
            raise exceptions.NotFound(detail=detail)

        try:
            applicants = request.data['applicants']
        except KeyError:
            raise exceptions.ValidationError('"applicants" field is mandatory')

        findings = ruleset.apply_to(applicants)

        return Response({
            'program': program,
            'entity': entity,
            'findings': findings,
        })
