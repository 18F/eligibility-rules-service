from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ruleset


class RulingsView(APIView):
    def post(self, request, program, entity, format=None):
        applicants = request.data['applicants']
        return Response({
            'program': program,
            'entity': entity,
            'payload': request.data,
            'findings': [
                'ok',
            ] * len(applicants)
        })
