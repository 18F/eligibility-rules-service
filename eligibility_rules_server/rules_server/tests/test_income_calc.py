"""
Tests related to income calculations
"""

import pytest
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
def test_income_summed():

    url = '/rulings/benefit-program/ohio/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert not data['findings'][0]['accepted']
    assert 'Annual income' in data['findings'][0]['reasons'][0]['description']

    assert data['findings'][1]['accepted']

    assert not data['findings'][2]['accepted']
    assert 'must be a veteran' in data['findings'][2]['reasons'][0][
        'description']
