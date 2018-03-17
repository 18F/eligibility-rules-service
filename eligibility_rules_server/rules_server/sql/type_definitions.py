FINDING_TYPE_SQL = """
  CREATE TYPE finding AS
    ( qualifies   BOOLEAN,
      limitation  TEXT,
      explanation TEXT,
      priority    NUMERIC );
"""
