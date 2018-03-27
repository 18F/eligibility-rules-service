ANNUALIZE_FUNCTION_DEF = """
  CREATE OR REPLACE FUNCTION annualize(text) RETURNS integer AS $$
    SELECT
      CASE REPLACE(REPLACE(LOWER($1), 'ly', ''), '-', '')
                 WHEN 'annual' THEN 1
                 WHEN 'month' THEN 12
                 WHEN 'semimonth' THEN 24
                 WHEN 'twicemonth' THEN 24
                 WHEN 'biweek' THEN 26
                 WHEN 'week' THEN 52
      END;
  $$ LANGUAGE SQL;"""

FEDERAL_POVERTY_LEVEL_FUNCTION_DEF = """
  CREATE OR REPLACE FUNCTION federal_poverty_level(integer, text) RETURNS integer AS $$
    SELECT
      CASE UPPER($2)
        WHEN 'AK' THEN
          CASE
            WHEN ($1 = 1) THEN 27861
            WHEN ($1 = 2) THEN 37537
            WHEN ($1 = 3) THEN 47212
            WHEN ($1 = 4) THEN 56888
            WHEN ($1 = 5) THEN 66563
            WHEN ($1 = 6) THEN 76239
            WHEN ($1 = 7) THEN 85914
            WHEN ($1 = 8) THEN 95590
            WHEN ($1 > 8) THEN 76442 + (($1 - 8) * 9676)
          END
        WHEN 'HI' THEN
          CASE
            WHEN ($1 = 1) THEN 25641
            WHEN ($1 = 2) THEN 34540
            WHEN ($1 = 3) THEN 43438
            WHEN ($1 = 4) THEN 52337
            WHEN ($1 = 5) THEN 61235
            WHEN ($1 = 6) THEN 70134
            WHEN ($1 = 7) THEN 79032
            WHEN ($1 = 8) THEN 87931
            WHEN ($1 > 8) THEN 76442 + (($1 - 8) * 8899 )
          END
        ELSE
          CASE
            WHEN ($1 = 1) THEN 22311
            WHEN ($1 = 2) THEN 30044
            WHEN ($1 = 3) THEN 37777
            WHEN ($1 = 4) THEN 45510
            WHEN ($1 = 5) THEN 53243
            WHEN ($1 = 6) THEN 60976
            WHEN ($1 = 7) THEN 68709
            WHEN ($1 = 8) THEN 76442
            WHEN ($1 > 8) THEN 76442 + (($1 - 8) * 7733)
          END
        END;
  $$ LANGUAGE SQL;"""

# Thanks for last_day to Anvesh Patel, https://www.dbrnd.com/2017/01/postgresql-how-to-find-last-day-of-the-month/
LAST_DAY_FUNCTION_DEF = """
CREATE OR REPLACE FUNCTION last_day_of_month(DATE)
RETURNS DATE AS
$$
	SELECT (date_trunc('MONTH', $1) + INTERVAL '1 MONTH - 1 day')::DATE;
$$ LANGUAGE 'sql'
IMMUTABLE STRICT;
"""
