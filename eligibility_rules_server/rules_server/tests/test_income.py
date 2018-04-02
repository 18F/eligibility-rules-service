"""
Tests related to income calculations
"""

import json
from copy import deepcopy
from os.path import join

import pytest
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()

with open(join('examples', 'wic-federal0.json')) as infile:
    payload0 = json.load(infile)


@pytest.fixture(autouse=True)
def rule_models():
    call_command('loaddata', 'rules_server/fixtures/federal_wic.json')


@pytest.mark.django_db
def test_response_form():

    url = '/rulings/wic/federal/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    findings = response.json()['findings']

    assert len(findings) == 2
    assert len(findings['1']) == 4
    assert len(findings['2']) == 1

    for application in findings.values():
        for applicant in application.values():
            assert 'eligible' in applicant
            assert 'categories' in applicant
            assert 'requirements' in applicant
            assert 'income' in applicant['requirements']
            assert 'standard income' in applicant['requirements']['income'][
                'subfindings']
            assert applicant['eligible'] in (True, False)


@pytest.mark.django_db
def test_identity_required():

    url = '/rulings/wic/federal/'

    payload1 = deepcopy(payload0)
    for application in payload1:
        for applicant in application['applicants']:
            applicant['proof_of_identity'] = True
    response = client.post(url, payload1, format='json')
    n_true = 0
    for application in response.json()['findings'].values():
        for applicant in application.values():
            if applicant['eligible']:
                n_true += 1
            for explanation in applicant['requirements']['identity'][
                    'explanation']:
                assert 'identity requirements' not in explanation
    assert n_true > 0

    payload1 = deepcopy(payload0)
    for application in payload1:
        for applicant in application['applicants']:
            applicant['proof_of_identity'] = False
    response = client.post(url, payload1, format='json')
    for application in response.json()['findings'].values():
        for applicant in application.values():
            assert not applicant['eligible']
