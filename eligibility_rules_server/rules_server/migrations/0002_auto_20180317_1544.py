# Generated by Django 2.0.3 on 2018-03-17 15:44

from django.db import migrations

from rules_server.sql.sql_function_defs import (ANNUALIZE_FUNCTION_DEF,
                                                FEDERAL_POVERTY_LEVEL_FUNCTION_DEF)
from rules_server.sql.type_definitions import FINDING_TYPE_SQL


class Migration(migrations.Migration):

    dependencies = [
        ('rules_server', '0001_initial'),
    ]

    sql = (ANNUALIZE_FUNCTION_DEF, FEDERAL_POVERTY_LEVEL_FUNCTION_DEF,
           FINDING_TYPE_SQL)

    operations = [migrations.RunSQL(sql)]
