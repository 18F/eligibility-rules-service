import factory
from . import models

class RulesetFactory(factory.Factory):
    class Meta:
        model = models.Ruleset

    program = factory.Faker('word')
    entity = factory.Faker('state_abbr')


class RuleFactory(factory.Factory):
    class Meta:
        model = models.Rule

    order = factory.Faker('pyint')
    name = factory.Faker('words')
    code = factory.Faker('pystr', max_chars=5)
    explanation = factory.Faker('sentence')
    ruleset = factory.SubFactory(RulesetFactory)
