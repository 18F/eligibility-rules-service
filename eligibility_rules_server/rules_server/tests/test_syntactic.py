import pytest
from rest_framework import exceptions

from rules_server.models import Ruleset, SyntaxSchema


@pytest.fixture(autouse=True)
def rule_models():

    rs0 = Ruleset(
        program='syntactic',
        entity='syntactic',
        sample_input=[{
            "id": 1,
            "foo": 0
        }])
    rs0.save()

    ss0 = SyntaxSchema(
        ruleset=rs0,
        code={
            'items': {
                'properties': {
                    'id': {
                        'type': 'integer'
                    },
                    'foo': {
                        'type': 'integer'
                    }
                },
                'type': 'object'
            },
            'type': 'array'
        })
    ss0.save()


payload0 = [{'id': 1, 'foo': 100}]


@pytest.mark.django_db
def test_valid_syntax_passes():

    rs = Ruleset.objects.get(program='syntactic', entity='syntactic')
    rs.validate(payload0)


@pytest.mark.django_db
def test_invalid_syntax_fails():

    payload1 = [{'id': 1, 'foo': 'bar'}]

    rs = Ruleset.objects.get(program='syntactic', entity='syntactic')
    with pytest.raises(exceptions.ParseError):
        rs.validate(payload1)
