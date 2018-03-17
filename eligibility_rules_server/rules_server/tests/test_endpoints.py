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
        summarizer="""
                              select inc.applicants_id,
                       (inc.findings).qualifies or (adj.findings).qualifies,
                       ARRAY_AGG((inc.findings).limitation),
                       ARRAY_AGG((inc.findings).explanation) || ARRAY_AGG((adj.findings).explanation)
                from   adjunct_income_source adj
                join   income_source inc on (inc.applicants_id = adj.applicants_id)
                group by 1, 2
              """,
        sample_input="""
[
  {
    "id": 2,
    "number_in_economic_unit": 1,
    "referrer_state": "AK",
    "income": [
      {
        "dollars": 11480.5,
        "frequency": "bi-weekly",
        "source": "wages-and-salary",
        "verified": true
      }
    ],
    "applicants": [
      {
        "id": 6
      }
    ]
  }
]
""")

    rs0.save()

    r00 = Rule(
        ruleset=rs0,
        ruleset_id=rs0.id,
        name='income',
        code="""
            , source AS
                (  select a2.id AS applicants_id,
                            SUM(ANNUALIZE(i.frequency) * i.dollars) AS annual_income,
                            FEDERAL_POVERTY_LEVEL(
                                a.number_in_economic_unit,
                                a.referrer_state) AS poverty_level,
                            a.number_in_economic_unit,
                            a.referrer_state
                    FROM income i
                    JOIN applications a ON (i.applications_id = a.id)
                    JOIN applicants a2 ON (a2.applications_id = a.id)
                    GROUP BY 1, 3, 4, 5
                    )
            select applicants_id,
                CASE WHEN annual_income <= 1.85 * poverty_level THEN ROW(true, null, 'Household annual income ' || annual_income::money || ' within 185%% of federal poverty level (' ||
                                                                            poverty_level::money || ' for ' || number_in_economic_unit || ' residents in ' || referrer_state || ')',
                                                                            10)::finding
                                                                ELSE ROW(false, null, 'Household annual income ' || annual_income::money || ' exceeds 185%% of federal poverty level (' ||
                                                                            poverty_level::money || ' for ' || number_in_economic_unit || ' residents in ' || referrer_state || ')',
                                                                            10)::finding END
                    AS findings
            from source
        """)
    r01 = Rule(
        ruleset=rs0,
        ruleset_id=rs0.id,
        name='adjunct_income',
        code="""
            , source as (
                select a.id AS applicants_id,
                    count(aie.program) AS n_programs,
                    ARRAY_AGG(aie.program) AS program_names
                from   applicants a
                left outer join adjunct_income_eligibility aie ON (aie.applicants_id = a.id)
                group by 1
            )
        select applicants_id,
                    CASE n_programs WHEN 0 THEN ROW(false, NULL, 'No adjunct program qualifications', 0)::finding
                                        ELSE ROW(true, NULL, 'Qualifies for ' || program_names::text, 20)::finding
                                    END AS findings
        from source
        """)

    r00.save()
    r01.save()


payload0 = [{
    'applicants': [{
        'adjunct_income_eligibility': [{
            'program': 'snap',
            'verified': True
        }, {
            'program': 'medicaid',
            'verified': True
        }],
        'id':
        1
    }, {
        'id': 2
    }, {
        'adjunct_income_eligibility': [{
            'program': 'snap',
            'verified': 'Excepted'
        }],
        'id':
        3
    }, {
        'id': 4
    }],
    'id':
    1,
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
}, {
    'applicants': [{
        'id': 6
    }],
    'id':
    2,
    'income': [{
        'dollars': 11480.5,
        'frequency': 'bi-weekly',
        'source': 'wages-and-salary',
        'verified': True
    }],
    'number_in_economic_unit':
    1,
    'referrer_state':
    'AK'
}]


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
    assert len(data['findings']) == 5


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
        for applicant in application['applicants']:
            assert applicant['id'] in [
                a['applicant_id'] for a in data['findings']
            ]


@pytest.mark.django_db
def test_sql_endpoint():
    """Verify that /program/entity/sql/ endpoint exists"""

    url = '/rulings/wic/federal/sql/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'JSON_TO_RECORDSET' in response.data
