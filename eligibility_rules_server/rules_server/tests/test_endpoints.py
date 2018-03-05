import hypothesis.strategies as st
import pytest
from hypothesis import given, settings
from rest_framework import status
from rest_framework.test import APIClient

from rules_server.factories import RuleFactory, RulesetFactory, Definition

client = APIClient()


@pytest.fixture(autouse=True)
def rule_models():
    rs0 = RulesetFactory(
        program='benefit-program',
        entity='ohio',
        record_spec="""id bigint, annual_income numeric,
                       veteran bool, number_in_family smallint""")
    rs0.save()

    d01 = Definition(ruleset=rs0, term='poverty', code='annual_income < 22000')
    d01.save()

    r00 = RuleFactory(
        ruleset_id=rs0.id,
        ruleset=rs0,
        code='annual_income < 30000',
        explanation='Income must be below $30,000 annually')
    r00.save()
    r01 = RuleFactory(
        ruleset_id=rs0.id,
        ruleset=rs0,
        code='veteran',
        explanation='Applicant must be a veteran')
    r01.save()
    r02 = RuleFactory(
        ruleset_id=rs0.id,
        ruleset=rs0,
        code='poverty',
        explanation='Applicant must fall below poverty line')
    r02.save()


@pytest.mark.django_db
def test_endpoint_exists():
    """Endpoint exists, and echoes back args from URL"""

    url = '/rulings/benefit-program/ohio/'
    payload = {
        'applicants': [
            {
                'id': 1,
                'annual_income': 30000,
                'veteran': True,
            },
        ]
    }
    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['program'] == 'benefit-program'
    assert data['entity'] == 'ohio'


@pytest.mark.django_db
def test_nonexistent_ruleset_raises():
    """Asking for a ruleset that does not exist raises 404"""

    payload = {
        'applicants': [
            {
                'id': 1,
                'annual_income': 30000,
                'veteran': True,
            },
        ]
    }
    url = '/rulings/benefit-program/no-such-state/'
    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = '/rulings/no-such-program-/ohio/'
    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = '/rulings/benefit-program/no-such-state/'
    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_one_response_per_applicant():
    """Endpoint gives a response for each submitted applicant"""

    url = '/rulings/benefit-program/ohio/'
    payload = {
        'applicants': [
            {
                'id': 1,
                'annual_income': 30000,
                'veteran': True,
            },
            {
                'id': 2,
                'annual_income': 35000,
                'number_in_family': 3,
            },
            {
                'id': 3,
                'annual_income': 25000,
                'number_in_family': 2,
            },
        ]
    }
    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['program'] == 'benefit-program'
    assert data['entity'] == 'ohio'
    assert len(data['findings']) == 3


@pytest.mark.django_db
def test_definition_used():
    """Rule referencing a definition is used and appears in results"""

    url = '/rulings/benefit-program/ohio/'
    payload = {
        'applicants': [
            {
                'id': 1,
                'annual_income': 30000,
                'veteran': True,
            },
            {
                'id': 2,
                'annual_income': 20000,
                'veteran': False,
            },
        ]
    }
    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    descriptions = [r['description'] for r in data['findings'][0]['reasons']]
    assert 'Applicant must fall below poverty line' in descriptions
    descriptions = [r['description'] for r in data['findings'][1]['reasons']]
    assert 'Applicant must fall below poverty line' not in descriptions


@settings(deadline=1000)
@given(
    st.lists(
        st.fixed_dictionaries({
            'id':
            st.integers(
                min_value=-9223372036854775808,
                max_value=9223372036854775807),  # pg bigint limits
            'annual_income':
            st.decimals(
                allow_nan=False,
                max_value=999999999999,
                min_value=-999999999999),
            'number_in_family':
            st.integers(min_value=0, max_value=1000),
            'veteran':
            st.booleans(),
        })))
@pytest.mark.django_db
def test_hypothesis_payload(applicants):
    """Use Hypothesis to try randomized edge-case payloads"""

    url = '/rulings/benefit-program/ohio/'
    payload = {'applicants': applicants}

    response = client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data['findings']) == len(applicants)
