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

with open(join('rules_server', 'sample_payloads',
               'wic-federal0.json')) as infile:
    payload0 = json.load(infile)


@pytest.fixture(autouse=True)
def rule_models():
    call_command('loaddata', 'rules_server/fixtures/federal_wic.json')


@pytest.mark.django_db
def test_income_summed():

    url = '/rulings/wic/federal/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    findings = response.json()['findings']

    assert len(findings) == 2
    assert len(findings['1']) == 4
    assert len(findings['2']) == 1

    for (key, val) in findings['1'].items():
        assert val['eligible']
    for (key, val) in findings['2'].items():
        assert not val['eligible']

    assert 'explanation' in findings['1']['1']['requirements']['income']
    assert 'explanation' in findings['1']['1']['requirements']['income'][
        'subfindings']['standard income']


@pytest.mark.django_db
def test_identity_required():

    url = '/rulings/wic/federal/'
    payload1 = deepcopy(payload0)
    payload1[0]['applicants'][1]['proof_of_identity'] = 'True'
    response = client.post(url, payload1, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['findings']['1']['1']['eligible']

    payload1[0]['applicants'][0]['proof_of_identity'] = 'False'
    response = client.post(url, payload1, format='json')
    assert not response.json()['findings']['1']['1']['eligible']
