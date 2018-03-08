ANNUALIZE_FUNCTION_DEF = """
  CREATE OR REPLACE FUNCTION annualize(text) RETURNS integer AS $$
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
