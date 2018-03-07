
ANNUALIZE_FUNCTION_DEF = """
  CREATE or replace FUNCTION annualize(text) RETURNS integer AS $$
    SELECT
      CASE LOWER(REPLACE($1, '-', ''))
                 WHEN 'annual' THEN 1
                 WHEN 'monthly' THEN 12
                 WHEN 'semimonthly' THEN 24
                 WHEN 'twicemonthly' THEN 24
                 WHEN 'biweekly' THEN 26
                 WHEN 'weekly' THEN 52
      END;
  $$ LANGUAGE SQL;"""


