# Generated by Django 2.0.2 on 2018-03-02 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_server', '0003_ruleset_record_spec'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='qualifies',
            field=models.TextField(null=True),
        ),
    ]
