import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from rest_framework.exceptions import ValidationError

from rules_server.models import Ruleset, Rule, SyntaxSchema

client = APIClient()


@pytest.fixture(autouse=True)
def rule_models():

    rs0 = Ruleset(
        program='syntactic',
        entity='syntactic',
        summarizer="select * from acceptall_source",
        sample_input="""[{"id": 1, "foo": 0}]""")
    rs0.save()

    r00 = Rule(name='acceptall', ruleset=rs0, code="""
        select id as applicants_id, ROW(true, null, 'OK', 0)::finding
        from   applications""")
    r00.save()

    ss0 = SyntaxSchema(ruleset=rs0, code=json.dumps(
        {'items': {'properties': {'id': {'type': 'integer'},
                                  'foo': {'type': 'integer'}},
                'type': 'object'},
        'type': 'array'}
        ))
    ss0.save()

payload0 = [{
    'id': 1,
    'foo': 100}]


@pytest.mark.django_db
def test_valid_syntax_passes():

    url = '/rulings/syntactic/syntactic/'
    response = client.post(url, payload0, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['program'] == 'syntactic'
    assert data['entity'] == 'syntactic'

@pytest.mark.django_db
def test_invalid_syntax_fails():

    url = '/rulings/syntactic/syntactic/'
    payload1 = [{ 'id': 1, 'foo': 'bar'}]
    response = client.post(url, payload1, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not of type 'integer'" in response.data['detail']

