from django.db import models


class Ruleset(models.Model):
    program = models.TextField(null=False, blank=False)
    entity = models.TextField(null=False, blank=False)

    # TODO: keep old rulesets when rules change?

class Rule(models.Model):
    name = models.TextField(null=False, blank=False)
    code = models.TextField(null=False, blank=False)
    explanation = models.TextField(null=False, blank=False)
    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE)

    # TODO: Parameterization, for similar rules with simple differences
