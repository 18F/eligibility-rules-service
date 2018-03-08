from rest_framework import serializers

from rules_server.models import Rule, Ruleset


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'


class RulesetSerializer(serializers.ModelSerializer):

    rule_set = RuleSerializer(many=True, read_only=True)

    class Meta:
        model = Ruleset
        fields = ('id', 'program', 'entity', 'record_spec', 'rule_set')
