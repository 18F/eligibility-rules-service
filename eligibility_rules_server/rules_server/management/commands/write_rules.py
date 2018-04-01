
import logging
import json

from django.core.management.base import BaseCommand
from django.db import connection
from rules_server.models import *

logger = logging.getLogger('console')



class Command(BaseCommand):
    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):
        clear()
        wic_federal()
        wic_az()




def clear():

    Rule.objects.all().delete()
    Ruleset.objects.all().delete()
    SyntaxSchema.objects.all().delete()



def wic_federal():

    with open('examples/wic-federal0.json') as infile:
        sample_input = json.load(infile)
    with open('rules_server/rules/wic-schema.json') as infile:
        raw_jsonschema = json.load(infile)

    rs0 = Ruleset(
        program='wic',
        entity='federal',
        sample_input=sample_input,
        null_sources={
            'income':
            """unnest(array[0]::numeric[], array['annual']::text[],
                                array['None']::text[], array[True]::text[])
            as t(dollars, frequency, source, verified) """,
            'adjunct_income_eligibility':
            'unnest(array[]::text[], array[]::text[]) as t(program, verified)',
        })
    rs0.save()

    ssch = SyntaxSchema(
        ruleset=rs0, code=raw_jsonschema)
    ssch.save()



    n1 = Node(
        ruleset=rs0,
        name='identity',
        parent=None,
        requires_all=True,
    )
    n1.save()

    r11 = Rule(
        name='proof of identity',
        node=n1,
        code="""
        select
            CASE proof_of_identity
            WHEN 'true' THEN
                ROW(true, NULL, 'Proof of identity supplied')::finding
            WHEN 'Exception' THEN
                ROW(true, NULL, 'Applicant must confirm his/her identity in writing')::finding
            ELSE
                ROW(false, NULL, 'Applicant does not meet identity requirements')::finding
            END AS result
        from applicant
        """)
    r11.save()

    r12 = Rule(
        name='all applicants physically present',
        node=n1,
        code="""
        select
            CASE all_applicants_present
            WHEN 'true' THEN
                ROW(true, NULL, 'All applicants physically present')::finding
            WHEN 'Exception' THEN
                ROW(true, NULL, 'Applicant not physically present, but exception provided')::finding
            ELSE
                ROW(false, NULL, 'Applicant not physically present')::finding
            END AS result
        from applicant
        """)
    r12.save()

    n2 = Node(
        ruleset=rs0,
        name='residential',
        parent=None,
        requires_all=True,
    )
    n2.save()

    r211 = Rule(
        name='proof of residency',
        node=n2,
        code="""
        select
            CASE proof_of_residence
            WHEN 'true' THEN
                ROW(true, null,
                'Applicant provided proof of residency within state')::finding
            WHEN 'Exception' THEN
                ROW(true, null,
                'Applicant must confirm his/her residency in writing')::finding
            ELSE
                ROW(false, null,
                'Applicant has not proven residence within state')::finding
            END AS result
        from applicant
        """)
    r211.save()

    r22121 = Rule(
        name='homeless residence will not benefit',
        node=n2,
        code="""
        select
            CASE homeless_residence
            WHEN 'false' THEN
                ROW(true, null,
                'Applicant does not live in a homeless institution')::finding
            WHEN 'true' THEN
                CASE homeless_residence_will_not_benefit
                WHEN 'false' THEN
                    ROW(false, null,
                    'Homeless institution cannot accrue financial benefit')::finding
                ELSE
                    ROW(true, null,
                    'Homeless institution will not accrue financial benefit')::finding
                END
            END AS result
        from applicant
        """)
    r22121.save()

    r22122 = Rule(
        name='homeless residence foods will not comingle',
        node=n2,
        code="""
        select
            CASE homeless_residence
            WHEN 'false' THEN
                ROW(true, null,
                'Applicant does not live in a homeless institution')::finding
            WHEN 'true' THEN
                CASE homeless_residence_foods_will_not_comingle
                WHEN 'false' THEN
                    ROW(false, null,
                    'Foods provided by WIC cannot be commingled with other food in homeless institution')::finding
                ELSE
                    ROW(true, null,
                    'Foods provided by WIC will not be commingled with other food in homeless institution')::finding
                END
            END AS result
        from applicant
        """)
    r22122.save()

    r22123 = Rule(
        name='homeless residence does not constrain wic',
        node=n2,
        code="""
        select
            CASE homeless_residence
            WHEN 'false' THEN
                ROW(true, null,
                'Applicant does not live in a homeless institution')::finding
            WHEN 'true' THEN
                CASE homeless_residence_does_not_constrain_wic
                WHEN 'false' THEN
                    ROW(false, null,
                    'Homeless institution cannot place constraints on WIC involvement')::finding
                ELSE
                    ROW(true, null,
                    'Homeless institution does place constraints on WIC involvement')::finding
                END
            END AS result
        from applicant
        """)
    r22123.save()

    n3 = Node(
        ruleset=rs0,
        name='categories',
        parent=None,
        requires_all=False,
    )
    n3.save()

    r312 = Rule(
        name='pregnant',
        node=n3,
        code="""
        select
            CASE currently_pregnant
            WHEN 'true' THEN
                ROW(true,
                ROW(null, true, 'to the last day of the month in which the infant becomes six weeks old or the pregnancy ends',
                'A pregnant woman will be certified for the duration of her pregnancy, and up to the last day of the month in which the infant becomes six weeks old or the pregnancy ends. - 7 CFR 246.7 (g)(1)(i)'
                )::limitation,
                'Woman currently pregnant')::finding
            ELSE
                ROW(false, NULL, 'Not pregnant woman')::finding
            END AS result
        from applicant
        """)
    r312.save()

    r313 = Rule(
        name='postpartum',
        node=n3,
        code="""
        select
            CASE WHEN
            date_birth_or_pregnancy_end >= (current_date - interval '1 year')
            AND
            (NOT breastfeeding)
            AND
            last_day_of_month((date_birth_or_pregnancy_end + interval '6 months')::date) >= current_date
            THEN
            ROW(true, ROW(last_day_of_month((date_birth_or_pregnancy_end + interval '6 months')::date), true,
                            'A postpartum woman will be certified up to the last day of the sixth month after the baby is born or the pregnancy ends (postpartum)',
                            'A postpartum woman will be certified up to the last day of the sixth month after the baby is born or the pregnancy ends (postpartum). - 7 CFR 246.7 (g)(1)(ii)'
                            )::limitation,
                            'Woman is postpartum')::finding
            ELSE
                ROW(false, NULL,
                    'A pregnant woman will be certified for the duration of her pregnancy, and up to the last day of the month in which the infant becomes six weeks old or the pregnancy ends. - 7 CFR 246.7 (g)(1)(i)'
                )::finding
            END AS result
        from applicant
        """)
    r313.save()

    r314 = Rule(
        name='breastfeeding',
        node=n3,
        code="""
        select
            CASE WHEN
            ((NOT currently_pregnant) OR (currently_pregnant IS NULL))
            AND
            breastfeeding
            AND
            date_birth_or_pregnancy_end <= current_date
            AND
            current_date <= last_day_of_month((date_birth_or_pregnancy_end + interval '6 months')::date)
            THEN
            ROW(true, ROW(last_day_of_month((date_birth_or_pregnancy_end + interval '6 months')::date), true,
                            'to the last day of the month in which the infant becomes six weeks old or the pregnancy ends',
                            'A breastfeeding woman will be certified up to the last day of the sixth month ('
                            || last_day_of_month((date_birth_or_pregnancy_end + interval '6 months')::date)
                            || ') after the baby is born ('
                            || date_birth_or_pregnancy_end
                            || ') or until the woman ceases breastfeeding, whichever occurs first.'
                            )::limitation,
                            'Woman is breastfeeding')::finding
            ELSE
                ROW(false, NULL,
                            'A breastfeeding woman will be certified up to the last day of the sixth month ('
                            || last_day_of_month((date_birth_or_pregnancy_end + interval '6 months')::date)
                            || ') after the baby is born ('
                            || date_birth_or_pregnancy_end
                            || ') or until the woman ceases breastfeeding, whichever occurs first.'
                )::finding
            END AS result
        from applicant
        """)
    r314.save()

    r322 = Rule(
        name='infant',
        node=n3,
        code="""
        select
            CASE
            WHEN current_date BETWEEN birthdate AND last_day_of_month((birthdate + interval '6 months')::date)
            THEN
                ROW(true,
                ROW(last_day_of_month((birthdate + interval '6 months')::date),
                    true,
                    'Certification date is between child’s birth date and the last day of the month in which the infant turns six months.',
                    'A child will be certified as an infant up to the last day of the month in which the infant turns six months.'
                    )::limitation,
                'Certified as an infant until ' || last_day_of_month((birthdate + interval '6 months')::date)
                || ', the last day of the month six months after the birthdate ('
                || birthdate || ')'
                )::finding
            ELSE
                ROW(false, NULL, 'Current date is after '
                    || last_day_of_month((birthdate + interval '6 months')::date)
                    || ', the last day of the month six months after the birthdate ('
                    || birthdate || ')'
                )::finding
            END AS result
        from applicant
        """)
    r322.save()


    r323 = Rule(
        name='child',
        node=n3,
        code="""
        select
            CASE
            WHEN current_date BETWEEN (birthdate + interval '1 year')::date
                                AND last_day_of_month((birthdate + interval '5 years')::date)
            THEN
            ROW(true,
                ROW(LEAST(last_day_of_month((birthdate + interval '5 years')::date),
                        (current_date + interval '6 months')::date),
                    true,
                    'A child will be certified as a child for six month periods from the first birthday ending with the last day of the month in which a child reaches his/her fifth birthday.',
                    'Certified until the earlier of six months from certification date ('
                    || (current_date + interval '6 months')::date
                    || ') and the last day of the month in which a child reaches his/her fifth birthday ('
                    || last_day_of_month((birthdate + interval '5 years')::date) || ').'
                )::limitation,
            'Certification date is after child’s first birthday and before its fifth birthday.'
            )::finding
            ELSE
                ROW(false, NULL,
                    'Current date is not between first birthday ('
                    || (birthdate + interval '1 year')::date
                    || ') and last day of month with fifth birthday ('
                    || last_day_of_month((birthdate + interval '5 years')::date)
                    || ').'
                )::finding
            END AS result
        from applicant
        """)
    r323.save()


    n4 = Node(
        ruleset=rs0,
        name='income',
        parent=None,
        requires_all=False,
    )
    n4.save()

    r6 = Rule(
        name='standard income',
        node=n4,
        code='''
        , total_income as (
            select SUM(ANNUALIZE(i.frequency) * i.dollars) AS annual_income,
                FEDERAL_POVERTY_LEVEL(
                                a.number_in_economic_unit,
                                a.referrer_state) AS poverty_level,
                            a.number_in_economic_unit,
                            a.referrer_state
                    FROM income i
                    CROSS JOIN applicant a  -- only one applicant row anyway
                    GROUP BY 2, 3, 4)
        select
                CASE WHEN annual_income <= 1.85 * poverty_level THEN ROW(true, null, 'Household annual income ' || annual_income::money || ' within 185%% of federal poverty level (' ||
                                                                            poverty_level::money || ' for ' || number_in_economic_unit || ' residents in ' || referrer_state || ')'
                                                                            )::finding
                                                                ELSE ROW(false, null, 'Household annual income ' || annual_income::money || ' exceeds 185%% of federal poverty level (' ||
                                                                            poverty_level::money || ' for ' || number_in_economic_unit || ' residents in ' || referrer_state || ')'
                                                                            )::finding END AS result
        from total_income
        ''',
    )
    r6.save()

    r42 = Rule(
        name='adjunct income eligibility',
        node=n4,
        code="""
        select
            CASE count(program) WHEN 0 THEN
                ROW(false, NULL, 'No adjunct program qualifications')::finding
            ELSE
                ROW(true, NULL, 'Qualifies for ' || ARRAY_TO_STRING(ARRAY_AGG(program), ', '))::finding
            END AS result
        from adjunct_income_eligibility
        """)
    r42.save()


def wic_az():


    with open('examples/wic-federal0.json') as infile:
        sample_input = json.load(infile)
    with open('rules_server/rules/wic-schema.json') as infile:
        raw_jsonschema = json.load(infile)

    rsaz = Ruleset(
        program='wic',
        entity='az',
        sample_input="",
        null_sources={
            'income':
            """unnest(array[0]::numeric[], array['annual']::text[],
                                array['None']::text[], array[True]::text[])
            as t(dollars, frequency, source, verified) """,
            'adjunct_income_eligibility':
            'unnest(array[]::text[], array[]::text[]) as t(program, verified)',
        })
    rsaz.save()

    ssch = SyntaxSchema(
        ruleset=rsaz, code=raw_jsonschema)
    ssch.save()


    n1 = Node(
        ruleset=rsaz,
        name='identity',
        parent=None,
        requires_all=True,
    )
    n1.save()

    az_30_days = """
                ROW(true,
                    ROW((current_date + interval '30 days')::date,
                    false,
                        '%(needed)s needed before '
                        || (current_date + interval '30 days')::date,
                    '%(failure)s'
                    )::limitation,
                    '%(failure)s')::finding
    """

    r11 = Rule(
        name='proof of identity',
        node=n1,
        code="""
        select
            CASE proof_of_identity
            WHEN 'true' THEN
                ROW(true, NULL, 'Proof of identity supplied')::finding
            WHEN 'Exception' THEN
                ROW(true, NULL, 'Applicant must confirm his/her identity in writing')::finding
            ELSE
    %s
            END AS result
        from applicant
        """ % (az_30_days % {'needed': 'Proof of identity',
                            'failure': 'Applicant does not meet identity requirements'})
    )

    r11.save()

    r12 = Rule(
        name='all applicants physically present',
        node=n1,
        code="""
        select
            CASE all_applicants_present
            WHEN 'true' THEN
                ROW(true, NULL, 'All applicants physically present')::finding
            WHEN 'Exception' THEN
                ROW(true, NULL,
                    'Not all applicants physically present.  Exception provided.'
                    || 'Applicant must provide medical documentation taken within 60 days')::finding
            ELSE
    %s
            END AS result
        from applicant
        """ % (az_30_days % {'needed': 'All applicants must appear in person',
                            'failure': 'Not all applicants physically present'})
    )
    r12.save()

    n2 = Node(
        ruleset=rsaz,
        name='residential',
        parent=None,
        requires_all=True,
    )
    n2.save()

    r211 = Rule(
        name='proof of residency',
        node=n2,
        code="""
        select
            CASE proof_of_residence
            WHEN 'true' THEN
                ROW(true, null,
                'Applicant provided proof of residency within state')::finding
            WHEN 'Exception' THEN
                ROW(true, null,
                'Applicant must confirm his/her residency in writing')::finding
            ELSE
                ROW(true,
                ROW((current_date + interval '30 days')::date, false,
                    'Proof of residency needed before ' || (current_date + interval '30 days')::date,
                    'Proof of residency needed before ' || (current_date + interval '30 days')::date
                )::limitation,
                'Proof of residency needed before ' || (current_date + interval '30 days')::date
                )::finding
            END AS result
        from applicant
        """ )
    r211.save()

    r22121 = Rule(
        name='homeless residence will not benefit',
        node=n2,
        code="""
        select
            CASE homeless_residence
            WHEN 'false' THEN
                ROW(true, null,
                'Applicant does not live in a homeless institution')::finding
            WHEN 'true' THEN
                CASE homeless_residence_will_not_benefit
                WHEN 'false' THEN
                    ROW(false, null,
                    'Homeless institution cannot accrue financial benefit')::finding
                ELSE
                    ROW(true, null,
                    'Homeless institution will not accrue financial benefit')::finding
                END
            END AS result
        from applicant
        """)
    r22121.save()

    r22122 = Rule(
        name='homeless residence foods will not comingle',
        node=n2,
        code="""
        select
            CASE homeless_residence
            WHEN 'false' THEN
                ROW(true, null,
                'Applicant does not live in a homeless institution')::finding
            WHEN 'true' THEN
                CASE homeless_residence_foods_will_not_comingle
                WHEN 'false' THEN
                    ROW(false, null,
                    'Foods provided by WIC cannot be commingled with other food in homeless institution')::finding
                ELSE
                    ROW(true, null,
                    'Foods provided by WIC will not be commingled with other food in homeless institution')::finding
                END
            END AS result
        from applicant
        """)
    r22122.save()

    r22123 = Rule(
        name='homeless residence does not constrain wic',
        node=n2,
        code="""
        select
            CASE homeless_residence
            WHEN 'false' THEN
                ROW(true, null,
                'Applicant does not live in a homeless institution')::finding
            WHEN 'true' THEN
                CASE homeless_residence_does_not_constrain_wic
                WHEN 'false' THEN
                    ROW(false, null,
                    'Homeless institution cannot place constraints on WIC involvement')::finding
                ELSE
                    ROW(true, null,
                    'Homeless institution does place constraints on WIC involvement')::finding
                END
            END AS result
        from applicant
        """)
    r22123.save()

    n3 = Node(
        ruleset=rsaz,
        name='categories',
        parent=None,
        requires_all=False,
    )
    n3.save()

    r312 = Rule(
        name='pregnant',
        node=n3,
        code="""
        select
            CASE currently_pregnant
            WHEN 'true' THEN
                ROW(true,
                ROW(null, true, 'A pregnant woman will be certified for the duration of her pregnancy, up to six (6) weeks postpartum',
                'A pregnant woman will be certified for the duration of her pregnancy, up to six (6) weeks postpartum'
                )::limitation,
                'Woman currently pregnant')::finding
            ELSE
                ROW(false, NULL, 'Not pregnant woman')::finding
            END AS result
        from applicant
        """)
    r312.save()

    r313 = Rule(
        name='postpartum',
        node=n3,
        code="""
        select
            CASE WHEN
            date_birth_or_pregnancy_end >= (current_date - interval '1 year')
            AND
            (NOT breastfeeding)
            AND
            (date_birth_or_pregnancy_end + interval '6 months')::date >= current_date
            THEN
            ROW(true, ROW((date_birth_or_pregnancy_end + interval '6 months')::date, true,
                            'until the infant becomes six weeks old or the pregnancy ends',
                            'A pregnant woman will be certified for the duration of her pregnancy, and until the infant becomes six months old or the pregnancy ends. - 7 CFR 246.7 (g)(1)(i)'
                            )::limitation,
                            'Woman is postpartum')::finding
            ELSE
                ROW(false, NULL,
                    'A pregnant woman will be certified for the duration of her pregnancy, and up to the last day of the month in which the infant becomes six weeks old or the pregnancy ends. - 7 CFR 246.7 (g)(1)(i)'
                )::finding
            END AS result
        from applicant
        """)
    r313.save()

    r314 = Rule(
        name='breastfeeding',
        node=n3,
        code="""
        select
            CASE WHEN
            ((NOT currently_pregnant) OR (currently_pregnant IS NULL))
            AND
            breastfeeding
            AND
            date_birth_or_pregnancy_end <= current_date
            AND
            current_date <= (date_birth_or_pregnancy_end + interval '1 year')::date
            THEN
            ROW(true, ROW((date_birth_or_pregnancy_end + interval '1 year')::date, true,
                            'up to the infant’s first birthday',
                            'to '
                            || (date_birth_or_pregnancy_end + interval '1 year')::date
                            || ' as breastfeeding woman up to the infant’s first birthday or until the woman ceases breastfeeding after six months postpartum, whichever occurs first.'
                            )::limitation,
                            'Woman is breastfeeding')::finding
            ELSE
                ROW(false, NULL,
                    'A breastfeeding woman will be certified up to the infant’s first birthday ('
                    || (date_birth_or_pregnancy_end + interval '1 year')::date
                    || ') or until the woman ceases breastfeeding after six months postpartum, whichever occurs first.'
                )::finding
            END AS result
        from applicant
        """)
    r314.save()

    r322 = Rule(
        name='infant',
        node=n3,
        code="""
        select
            CASE
            WHEN current_date BETWEEN birthdate AND (birthdate + interval '6 months')::date
            THEN
                ROW(true,
                ROW((birthdate + interval '1 year')::date,
                    true,
                    'A child less than six months at time of certification will be certified as an infant until the first birthday.',
                    'A child less than six months at time of certification will be certified as an infant until the first birthday ('
                    || (birthdate + interval '1 year')::date || ' ).'
                    )::limitation,
                'A child less than six months at time of certification will be certified as an infant until the first birthday.'
                )::finding
            WHEN current_date BETWEEN (birthdate + interval '6 months') AND (birthdate + interval '1 year')::date
            THEN
                ROW(true,
                ROW((current_date + interval '6 months')::date,
                    true,
                    'A child child more than six months at time of certification is certified as an infant for six months after certification date.',
                    'A child child more than six months at time of certification is certified as an infant for six months after certification date.'
                    )::limitation,
                    'A child child more than six months at time of certification is certified as an infant for six months after certification date.'
                )::finding
            ELSE
                ROW(false, NULL, 'Child is beyond first birthday ('
                    || (birthdate + interval '1 year')::date
                    || ').'
                )::finding
            END AS result
        from applicant
        """)
    r322.save()


    r323 = Rule(
        name='child',
        node=n3,
        code="""
        select
            CASE
            WHEN current_date BETWEEN (birthdate + interval '1 year')::date
                                AND last_day_of_month((birthdate + interval '5 years')::date)
            THEN
            ROW(true,
                ROW(LEAST(last_day_of_month((birthdate + interval '5 years')::date),
                        (current_date + interval '1 year')::date),
                    true,
                    'A child will be certified for one year periods, ending with the end of the month in which the child reaches five years of age.',
                    'A child will be certified for one year periods, '
                    || 'ending with the end of the month in which the child reaches five years of age ('
                    || last_day_of_month((birthdate + interval '5 years')::date)
                    || ').'
                )::limitation,
            'Certification date is after child’s first birthday and before its fifth birthday.'
            )::finding
            ELSE
                ROW(false, NULL,
                    'Current date is not between first birthday ('
                    || (birthdate + interval '1 year')::date
                    || ') and last day of month with fifth birthday ('
                    || last_day_of_month((birthdate + interval '5 years')::date)
                    || ').'
                )::finding
            END AS result
        from applicant
        """)
    r323.save()


    n4 = Node(
        ruleset=rsaz,
        name='income',
        parent=None,
        requires_all=False,
    )
    n4.save()

    r6 = Rule(
        name='standard income',
        node=n4,
        code='''
        , total_income as (
            select SUM(ANNUALIZE(i.frequency) * i.dollars) AS annual_income,
                FEDERAL_POVERTY_LEVEL(
                                a.number_in_economic_unit,
                                a.referrer_state) AS poverty_level,
                            a.number_in_economic_unit,
                            a.referrer_state
                    FROM income i
                    CROSS JOIN applicant a  -- only one applicant row anyway
                    GROUP BY 2, 3, 4)
        select
                CASE WHEN annual_income <= 1.85 * poverty_level THEN ROW(true, null, 'Household annual income ' || annual_income::money || ' within 185%% of federal poverty level (' ||
                                                                            poverty_level::money || ' for ' || number_in_economic_unit || ' residents in ' || referrer_state || ')'
                                                                            )::finding
                                                                ELSE ROW(false, null, 'Household annual income ' || annual_income::money || ' exceeds 185%% of federal poverty level (' ||
                                                                            poverty_level::money || ' for ' || number_in_economic_unit || ' residents in ' || referrer_state || ')'
                                                                            )::finding END AS result
        from total_income
        ''',
    )
    r6.save()


    r42 = Rule(
        name='adjunct income eligibility',
        node=n4,
        code="""
        , aggregated_income_eligiblility as (
            SELECT count(program) AS n_programs,
                   count(program) FILTER (WHERE verified = 'false') AS n_unverified,
                   ARRAY_AGG(program) AS programs,
                   ARRAY_AGG(program) FILTER (WHERE verified = 'false') AS unverified
            FROM   adjunct_income_eligibility
        )
        select
            CASE n_programs
            WHEN 0 THEN
                ROW(false, NULL, 'No adjunct program qualifications')::finding
            ELSE
                ROW(true,
                    CASE n_unverified
                    WHEN 0 THEN NULL
                    ELSE
                        ROW((current_date + interval '30 days')::date,
                            false,
                            'Applicant has stated but not verified adjunct income eligibility',
                            'Applicant must present verification for eligibility for '
                            || ARRAY_TO_STRING(unverified, ', ') || ' by '
                            || (current_date + interval '30 days')::date)::limitation
                    END,
                    'Qualifies for ' || ARRAY_TO_STRING(programs, ', '))::finding
            END AS result
        from aggregated_income_eligiblility
        """)

    r42.save()
