from rest_framework import status
from rest_framework.test import APITestCase


class TestRulingsEndpoint(APITestCase):
    def test_endpoint_exists(self):
        """Endpoint exists, and echoes back args from URL"""

        url = '/rulings/benefit-program/ohio/'
        payload = {'annual_income': 30000, 'veteran': True, }
        response = self.client.get(url, payload)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['program'] == 'benefit-program'
        assert data['entity'] == 'ohio'
