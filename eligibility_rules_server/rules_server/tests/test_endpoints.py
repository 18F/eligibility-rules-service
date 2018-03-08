from copy import deepcopy

import hypothesis.strategies as st
import pytest
from hypothesis import given, settings
from rest_framework import status
from rest_framework.test import APIClient

from rules_server.factories import RuleFactory, RulesetFactory

client = APIClient()


@pytest.fixture(autouse=True)
def rule_models():
    rs0 = RulesetFactory(
        program='benefit-program',
        entity='ohio',
        record_spec="""id bigint, income jsonb,
                       veteran bool, number_in_family smallint""")
    rs0.save()

    r00 = RuleFactory(
        ruleset_id=rs0.id,
        ruleset=rs0,
        code="annual_income < 20000",
        explanation="'Annual income ' || annual_income || ' exceeds 20000'",
        array_field='income',
        aggregate_definitions=", sum((income_elements->>'dollars')::numeric"
        " * ANNUALIZE(income_elements->>'frequency') ) AS annual_income")
    r00.save()

    r01 = RuleFactory(
        ruleset_id=rs0.id,
        ruleset=rs0,
        code='veteran',
        explanation="'Applicant must be a veteran'")
    r01.save()


payload0 = {
    'applicants': [
        {
            'id':
            1,
            'income': [{
                'dollars': 280.5,
                'frequency': 'bi-weekly',
                'type': 'wages-and-salary'
            }, {
                'dollars': 150.75,
                'frequency': 'weekly',
                'source': 'self-employment'
            }, {
                'dollars': 200,
                'frequency': 'semi-monthly',
                'source': 'social-security'
            }, {
                'dollars': 2000,
                'frequency': 'annually',
                'source': 'royalties'
            }, {
                'dollars': 200,
                'frequency': 'monthly',
                'source': 'alimony-and-child-support'
            }],
            'veteran':
            True,
            'number_in_family':
            5,
        },
        {
            'id':
            2,
            'income': [
                {
                    'dollars': 500,
                    'frequency': 'monthly',
                    'type': 'wages-and-salary'
                },
            ],
            'veteran':
            True,
            'number_in_family':
            2,
        },
        {
            'id': 3,
            'income': [],
            'veteran': False,
            'number_in_family': 1,
        },
    ],
}


@pytest.mark.django_db
def test_endpoint_exists():
    """Endpoint exists, and echoes back args from URL"""

    url = '/rulings/benefit-program/ohio/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['program'] == 'benefit-program'
    assert data['entity'] == 'ohio'


@pytest.mark.django_db
def test_nonexistent_ruleset_raises():
    """Asking for a ruleset that does not exist raises 404"""

    url = '/rulings/benefit-program/no-such-state/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = '/rulings/no-such-program-/ohio/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = '/rulings/benefit-program/no-such-state/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_one_response_per_applicant():
    """Endpoint gives a response for each submitted applicant"""

    url = '/rulings/benefit-program/ohio/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['program'] == 'benefit-program'
    assert data['entity'] == 'ohio'
    assert len(data['findings']) == 3


@pytest.mark.django_db
def test_definition_used():
    """Rule referencing a definition is used and appears in results"""

    url = '/rulings/benefit-program/ohio/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    description = [r['description'] for r in data['findings'][0]['reasons']][0]
    assert 'Annual income' in description
    assert not data['findings'][1]['reasons']


@settings(deadline=1000)
@given(
    st.integers(min_value=-9223372036854775808,
                max_value=9223372036854775807),  # pg bigint limits
)
@pytest.mark.django_db
def test_hypothesis_payload(applicant_data):
    """Use Hypothesis to try randomized edge-case payloads"""

    url = '/rulings/benefit-program/ohio/'
    payload = deepcopy(payload0)
    payload['applicants'][0]['income'][0]['dollars'] = applicant_data

    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data['findings']) == len(payload['applicants'])


@pytest.mark.django_db
def test_rule_endpoint():
    """Verify that /program/entity/rules endpoint exists"""

    url = '/rulings/benefit-program/ohio/rules/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['program'] == 'benefit-program'
    assert data['entity'] == 'ohio'
    assert 'rule_set' in data
    assert 'sql' in data
