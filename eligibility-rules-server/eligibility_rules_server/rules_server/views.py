from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


class RulingsView(APIView):
    def post(self, request, program, entity, format=None):
        return Response({'program': program, 'entity': entity, 'payload': request.data, 'results': ['ok', ]})

    def get(self, request, program, entity, format=None):
        return Response({'program': program, 'entity': entity, 'results': ['ok', ]})
