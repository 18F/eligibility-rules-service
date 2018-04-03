"""
Tests related to income calculations
"""

from copy import deepcopy

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from rules_server.models import Node, Rule, Ruleset

client = APIClient()

payload0 = [{
    "application_id":
    1,
    'applicants': [{
        'id':
        1,
        'income': [{
            'dollars': 100,
            'frequency': 'bi-weekly'
        }, {
            'dollars': 1000,
            'frequency': 'monthly'
        }, {
            'dollars': 5000,
            'frequency': 'annually'
        }]
    }]
}]


@pytest.fixture(autouse=True)
def rule_models():

    rs0 = Ruleset(
        program='program1',
        entity='state1',
        sample_input=payload0,
        null_sources={})
    rs0.save()

    n0 = Node(name='income', ruleset=rs0, requires_all=True)
    n0.save()

    r0 = Rule(
        node=n0,
        name='total income',
        code="""
        SELECT
          CASE
            WHEN SUM(dollars * annualize(frequency)) >
                 FEDERAL_POVERTY_LEVEL_185(1, 'state1')
            THEN
              ROW(false, null,
                  'Income ' || SUM(dollars * annualize(frequency))::money
                  || ' exceeds 185%% of Federal poverty level')::finding
            ELSE
              ROW(true, null,
                  'Income ' || SUM(dollars * annualize(frequency))::money
                  || ' is within 185%% of Federal poverty level')::finding
            END AS result
        FROM income""")
    r0.save()


@pytest.mark.django_db
def test_income_summed():

    url = '/rulings/program1/state1/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['findings']['1']['1']['eligible']
    assert 'within' in data['findings']['1']['1']['requirements']['income'][
        'explanation'][0]
    assert '$19,600.00' in data['findings']['1']['1']['requirements'][
        'income']['explanation'][0]

    # Now applicant strikes it rich
    payload1 = deepcopy(payload0)
    payload1[0]['applicants'][0]['income'][0]['dollars'] = 1000000
    response = client.post(url, payload1, format='json')
    data = response.json()
    assert not data['findings']['1']['1']['eligible']
