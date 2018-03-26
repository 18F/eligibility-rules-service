LIMITATION_TYPE_SQL = """
  CREATE TYPE limitation AS
  ( end_date     DATE,
    normal       BOOLEAN,
    description  TEXT,
    explanation  TEXT)
"""

FINDING_TYPE_SQL = """
  CREATE TYPE finding AS
    ( eligible    BOOLEAN,
      limitation  LIMITATION,
      explanation TEXT);
"""
