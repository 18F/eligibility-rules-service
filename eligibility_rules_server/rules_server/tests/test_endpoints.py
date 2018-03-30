import json
from copy import deepcopy
from os.path import join

import hypothesis.strategies as st
import pytest
from django.core.management import call_command
from hypothesis import given, settings
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()

with open(join('examples', 'wic-federal0.json')) as infile:
    payload0 = json.load(infile)


@pytest.fixture(autouse=True)
def rule_models():
    call_command('loaddata', 'rules_server/fixtures/federal_wic.json')


@pytest.mark.django_db
def test_endpoint_exists():
    """Endpoint exists, and echoes back args from URL"""

    url = '/rulings/wic/federal/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['program'] == 'wic'
    assert data['entity'] == 'federal'


@pytest.mark.django_db
def test_nonexistent_ruleset_raises():
    """Asking for a ruleset that does not exist raises 404"""

    url = '/rulings/wic/no-such-state/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = '/rulings/no-such-program-/federal/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = '/rulings/wic/no-such-state/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_one_response_per_applicant():
    """Endpoint gives a response for each submitted applicant"""

    url = '/rulings/wic/federal/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['program'] == 'wic'
    assert data['entity'] == 'federal'
    assert len(data['findings']) == 2


@settings(deadline=1000)
@given(
    st.integers(min_value=-2147483648,
                max_value=2147483647),  # pg regular int limits
)
@pytest.mark.django_db
def test_hypothesis_payload(applicant_data):
    """Use Hypothesis to try randomized edge-case payloads"""

    url = '/rulings/wic/federal/'
    payload = deepcopy(payload0)
    payload[0]['income'][0]['dollars'] = applicant_data

    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    for application in payload:
        application_id = str(application['application_id'])
        assert application_id in data['findings']
        for applicant in application['applicants']:
            assert str(applicant['id']) in data['findings'][application_id]


@pytest.mark.django_db
def test_sql_endpoint():
    """Verify that /program/entity/sql/ endpoint exists"""

    url = '/rulings/wic/federal/sql/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'JSON_TO_RECORDSET' in response.data
