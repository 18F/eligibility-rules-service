from copy import deepcopy

import hypothesis.strategies as st
import pytest
from hypothesis import given, settings
from rest_framework import status
from rest_framework.test import APIClient

from rules_server.models import Rule, Ruleset

client = APIClient()


@pytest.fixture(autouse=True)
def rule_models():

    rs0 = Ruleset(
        program='wic',
        entity='federal',
        sample_input="",
        null_sources={
            'income':
            """unnest(array[0]::numeric[], array['annual']::text[],
                                array['None']::text[], array[True]::text[])
              as t(dollars, frequency, source, verified) """,
            'adjunct_income_eligibility':
            'unnest(array[]::text[], array[]::text[]) as t(program, verified)',
        })
    rs0.save()

    n0 = Node(
        ruleset=rs0,
        name='income',
        parent=None,
        requires_all=False,
    )
    n0.save()

    r0 = Rule(
        name='standard income',
        node=n0,
        code='''
        , total_income as (
            select SUM(ANNUALIZE(i.frequency) * i.dollars) AS annual_income,
                   FEDERAL_POVERTY_LEVEL(
                                a.number_in_economic_unit,
                                a.referrer_state) AS poverty_level,
                            a.number_in_economic_unit,
                            a.referrer_state
                    FROM income i
                    CROSS JOIN applicant a  -- only one applicant row anyway
                    GROUP BY 2, 3, 4)
        select
                CASE WHEN annual_income <= 1.85 * poverty_level THEN ROW(true, null, 'Household annual income ' || annual_income::money || ' within 185%% of federal poverty level (' ||
                                                                            poverty_level::money || ' for ' || number_in_economic_unit || ' residents in ' || referrer_state || ')'
                                                                            )::finding
                                                                ELSE ROW(false, null, 'Household annual income ' || annual_income::money || ' exceeds 185%% of federal poverty level (' ||
                                                                            poverty_level::money || ' for ' || number_in_economic_unit || ' residents in ' || referrer_state || ')'
                                                                            )::finding END AS result
        from total_income
        ''',
    )
    r0.save()

    r1 = Rule(
        name='adjunct income eligibility',
        node=n0,
        code="""
        select
            CASE count(program) WHEN 0 THEN
                ROW(false, NULL, 'No adjunct program qualifications')::finding
            ELSE
                ROW(true, NULL, 'Qualifies for ' || ARRAY_TO_STRING(ARRAY_AGG(program), ', '))::finding
            END AS result
        from adjunct_income_eligibility
        """)
    r1.save()

    n1 = Node(
        ruleset=rs0,
        name='identity',
        parent=None,
        requires_all=True,
    )
    n1.save()

    r10 = Rule(
        name='proof of identity',
        node=n1,
        code="""
        select
            CASE proof_of_identity
            WHEN 'True' THEN
                ROW(true, NULL, 'Proof of identity supplied')::finding
            WHEN 'Exception' THEN
                ROW(true, NULL, 'Applicant must confirm his/her identity in writing')::finding
            ELSE
                ROW(false, NULL, 'No proof of identity supplied')::finding
            END AS result
        from applicant
        """)
    r10.save()


payload0 = {
    1:  # household 1
    {
        'applicants': {
            1: {
                'proof_of_identity':
                'True',
                'physically_present':
                'True',
                'adjunct_income_eligibility': [{
                    'program': 'snap',
                    'verified': True
                }, {
                                                   'program': 'medicaid',
                                                   'verified': True
                                               }],
                'id':
                1
            },
            2: {
                'physically_present': 'True',
                'proof_of_identity': 'True',
            },
            3: {
                'physically_present':
                'True',
                'proof_of_identity':
                'True',
                'adjunct_income_eligibility': [{
                    'program': 'snap',
                    'verified': 'Excepted'
                }],
            },
            4: {
                'physically_present': 'True',
                'proof_of_identity': 'True',
            },
        },
        'income': [{
            'dollars': 1480.5,
            'frequency': 'bi-weekly',
            'source': 'wages-and-salary',
            'verified': True
        }, {
                       'dollars': 150.75,
                       'frequency': 'weekly',
                       'source': 'self-employment',
                       'verified': False
                   }, {
                       'dollars': 200,
                       'frequency': 'semi-monthly',
                       'source': 'social-security',
                       'verified': 'Excepted'
                   }, {
                       'dollars': 2000,
                       'frequency': 'annually',
                       'source': 'royalties',
                       'verified': True
                   }, {
                       'dollars': 200,
                       'frequency': 'monthly',
                       'source': 'alimony-and-child-support',
                       'verified': False
                   }],
        'number_in_economic_unit':
        5,
        'referrer_state':
        'OH'
    },
    2: {
        'applicants': {
            6: {
                'physically_present':
                'True',
                'proof_of_identity':
                'True',
                'income': [{
                    'dollars': 11480.5,
                    'frequency': 'bi-weekly',
                    'source': 'wages-and-salary',
                    'verified': True
                }],
            },
        },
        'number_in_economic_unit': 1,
        'referrer_state': 'AK'
    }
}


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
    payload[1]['income'][0]['dollars'] = applicant_data

    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    for (application_id, application) in payload.items():
        for applicant_id in application['applicants'].keys():
            assert str(applicant_id) in data['findings'][str(application_id)]


@pytest.mark.django_db
def test_sql_endpoint():
    """Verify that /program/entity/sql/ endpoint exists"""

    url = '/rulings/wic/federal/sql/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'JSON_TO_RECORDSET' in response.data
