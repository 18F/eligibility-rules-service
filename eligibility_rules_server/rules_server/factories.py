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
    name = factory.Faker('text', max_nb_chars=20)
    code = 'x > 10'
    qualifies = None
    explanation = factory.Faker('sentence')
    ruleset = factory.SubFactory(RulesetFactory)


class Definition(factory.Factory):
    class Meta:
        model = models.Definition

    term = factory.Faker('word')
    code = 'x < 4'
    explanation = factory.Faker('sentence')
    ruleset = factory.SubFactory(RulesetFactory)
