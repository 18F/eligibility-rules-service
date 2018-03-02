import hypothesis.strategies as st
from hypothesis import given
from rest_framework import status
from rest_framework.test import APITestCase


class TestRulingsEndpoint(APITestCase):
    def test_endpoint_exists(self):
        """Endpoint exists, and echoes back args from URL"""

        url = '/rulings/benefit-program/ohio/'
        payload = {
            'applicants': [
                {
                    'annual_income': 30000,
                    'veteran': True,
                },
            ]
        }
        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['program'] == 'benefit-program'
        assert data['entity'] == 'ohio'

    def test_one_response_per_applicant(self):
        """Endpoint gives a response for each submitted applicant"""

        url = '/rulings/benefit-program/ohio/'
        payload = {
            'applicants': [
                {
                    'annual_income': 30000,
                    'veteran': True,
                },
                {
                    'annual_income': 35000,
                    'number_in_family': 3,
                },
                {
                    'annual_income': 25000,
                    'number_in_family': 2,
                },
            ]
        }
        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['program'] == 'benefit-program'
        assert data['entity'] == 'ohio'
        assert len(data['findings']) == 3

    @given(
        st.lists(
            st.fixed_dictionaries({
                'annual_income':
                st.decimals(
                    allow_nan=False,
                    max_value=999999999999,
                    min_value=-999999999999),
                'number_in_family':
                st.integers(),
                'veteran':
                st.booleans(),
            })))
    def test_hypothesis_payload(self, applicants):
        """Use Hypothesis to try randomized edge-case payloads"""

        url = '/rulings/benefit-program/ohio/'
        payload = {'applicants': applicants}

        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['findings']) == len(applicants)
