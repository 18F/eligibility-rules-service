# Guide for rule-writing

## Data structure

### Ruleset

Each combination of program (example: WIC) and entity
(example: Arizona) has a unique ruleset.

#### `null_sources`

SQL that depends on a sub-table may fail completely for applicants who don't
have any data for that table.  `null_sources` is a clunky solution for generating
needed empty rows.

### Node

Within a ruleset, rules are grouped in nodes.  `Node.requires_all`
determines whether the `eligibility` finding for the node comes from
combining the individual rules' results with `AND` or `OR`.

Nodes can have child nodes, useful for complex combinations of
boolean logic.

#### `categories` node

If there is a top-level node with `name=='categories'`, its
results will be reported separately from the other nodes'
results (which are grouped under `requirements` in the results),
and its `eligible` results will not affect the applicant's overall
eligibility.  Instead of overall eligibility, `categories` rules
are used to determine whether an applicant fits under cagtegories
like "infant", "child", "pregnant", etc.

### Rule

A rule's `code` is SQL that's run against a SQL `VALUES` statement
built from the JSON payload.  Each level within the payload becomes
a pseudo-table of the same name.  This is best illustrated with an
example.

Executing a rule's code *must* produce a single row of the
user-defined `finding` type, and it must be named `result`:

```
  CREATE TYPE finding AS
    ( eligible    BOOLEAN,
      limitation  LIMITATION,
      explanation TEXT);
```

The `limitation`, if present, is also a user-defined type:

```
  CREATE TYPE limitation AS
  ( end_date     DATE,
    normal       BOOLEAN,
    description  TEXT,
    explanation  TEXT)
```

The best way to understand this is to study and emulate the sample endpoints (below).


### SyntaxSchema

A JSON schema can be attached to a node.

SyntaxSchema is optional, but it serves two useful purposes:

1. Payloads are validated against the schema, and if they do not meet the required syntax, JSON schema validation errors are more comprehensible than the results of failures at the SQL level.

2. The schema's datatype is used to determine the SQL data type to be used.  Note that the schema is searched very simply for any particular column name, and if a field name appears at multiple places within the schema, there's no predicting which one will be used to set data types for that column.


## Authoring rules

Rulesets, nodes, rules, and SyntaxSchemas are all stored as records in
PostgreSQL, managed through the Django ORM.  At present, the means of
writing and saving rules is very primitive: they are hardcoded into
[write_rules.py](rules_server/management/commands/write_rules.py),
which is run with `python manage.py write_rules`.
This script also dumps the result into a [fixture file](rules_server/fixtures/federal_wic.json)
so that the data can easily be loaded into a new database instance
with `python manage.py loaddata rules_server/fixtures/federal_wic.json`.


## PostgreSQL

The API uses PostgreSQL, so you can write rules with rich
PostgreSQL syntax.  Features like ARRAY_AGG and filtered
aggregates are especially useful.

## Developer's endpoints

To help you visualize and troubleshoot, each ruleset exposes some specialty endpoints.  These
examples use the ruleset `sample/sample`, but they work for any ruleset created in the database
(a complex example is `wic/federal`).

- POSTing a payload to https://eligibility-rules.app.cloud.gov/rulings/sample/sample/sql/ prints out SQL
statements - first, the Common Table Expressions created from the payload data, together
with query results against those CTEs; then, the complete SQL statements used for each
rule.  GETting without a payload does the same, for the ruleset's `sample_input`.

- GET to https://eligibility-rules.app.cloud.gov/rulings/sample/sample/schema/ displays the ruleset's SyntaxSchema.

- GET to https://eligibility-rules.app.cloud.gov/rulings/sample/sample/sample/ displays the ruleset's sample input.
