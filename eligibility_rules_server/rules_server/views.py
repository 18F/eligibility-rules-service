import jsonschema
import sqlparse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ruleset
from .serializers import RulesetSerializer


class RulesetFinderMixin:
    def get_ruleset(self, program, entity):

        try:
            ruleset = Ruleset.objects.get(program=program, entity=entity)
        except Ruleset.DoesNotExist:
            detail = "Ruleset for program '{}', entity '{}'" \
                     "has not been defined".format(program, entity)
            raise exceptions.NotFound(detail=detail)

        return ruleset


class RulingsView(RulesetFinderMixin, APIView):
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

        ruleset = self.get_ruleset(program=program, entity=entity)

        for syntax_schema in ruleset.syntaxschema_set.all():
            try:
                jsonschema.validate(request.data, syntax_schema.code)
            except jsonschema.ValidationError as valerr:
                raise exceptions.ParseError(str(valerr))

        results = {}
        for application in request.data:
            results[int(
                application['application_id'])] = ruleset.calc(application)

        return Response({
            'program': program,
            'entity': entity,
            'findings': results,
        })


class RulesetView(RulesetFinderMixin, APIView):
    def get(self, request, program, entity, format=None):

        ruleset = self.get_ruleset(program=program, entity=entity)
        data = RulesetSerializer(ruleset).data
        data['sql'] = [
            sqlparse.format(r.sql(), reindent=True, keyword_case='upper')
            for r in ruleset.rule_set.all()
        ]
        return Response(data)


class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset)


class RulesetSqlView(RulesetFinderMixin, APIView):

    renderer_classes = (PlainTextRenderer, )

    @csrf_exempt
    def get(self, request, program, entity, format=None):
        ruleset = self.get_ruleset(program=program, entity=entity)
        return self.sql(
            request=request,
            payload=ruleset.sample_data,
            program=program,
            entity=entity,
            format=format)

    @csrf_exempt
    def post(self, request, program, entity, format=None):
        return self.sql(
            request=request,
            payload=request.data,
            program=program,
            entity=entity,
            format=format)

    def sql(self, payload, request, program, entity, format=None):
        result = []
        ruleset = self.get_ruleset(program=program, entity=entity)
        for application in payload:
            for sql in ruleset.source_sql_statements(application):
                result.append(sql)
            for sql in ruleset.sql(application):
                result.append(sql)
        return Response('\n\n\n'.join(result))


class RulesetSchemaView(RulesetFinderMixin, APIView):
    def get(self, request, program, entity, format=None):

        ruleset = self.get_ruleset(program=program, entity=entity)
        if ruleset.syntaxschema_set.count() == 1:
            return Response(ruleset.syntaxschema_set.first().code)
        else:
            return Response([s.code for s in ruleset.syntaxschema_set.all()])


class RulesetSampleView(RulesetFinderMixin, APIView):
    def get(self, request, program, entity, format=None):

        ruleset = self.get_ruleset(program=program, entity=entity)
        return Response(ruleset.sample_input)
