FINDING_TYPE_SQL = """
  CREATE TYPE finding AS
    ( eligible    BOOLEAN,
      limitation  TEXT,
      explanation TEXT);
"""
