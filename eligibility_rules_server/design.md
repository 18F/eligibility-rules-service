# Design notes

The current `eligibility_rules_server` code is a proof-of-concept
prototype demonstrating its use for delivering eligibility rulings
according to program rules for the Federal WIC program and its
Arizona state variant.

We hope that the prototype can be extended for production use and
for more

## Architecture

The API server is written in Django REST Framework and requires a
PostgreSQL back-end.

## Design principle

The server allows rules to be stored as records in PostgreSQL,
then applied to JSON payloads to produce a set of findings for each
applicant.  Information from the payloads themselves is never
stored on the server.

Rules are written in SQL, but the incoming data is never stored;
instead, it is used to generate SQL `VALUES` statements that the
rules query against.

## Payloads

The structure of payloads is defined only loosely: each request is a
list of applications, each of which contains a list of applicants:

```
[
  {
    "application_id": 1,
    "applicants": [
      {
        "id": 1,
        ...
      }
    ]
  }
]
```

However, any further details of the structure only depend on the
rules in a particular ruleset and that ruleset's JSON schema (if any).

An example of a specific detailed payload is in
[examples/wic-federal0.json](examples/wic-federal0.json).

### Application-level data

Data defined at the application level is "pushed down" into each applicant's data
before evaluation, though applicant-specific data supersedes application-level
data.  So, for instance, this payload:

```
[
  {
    "application_id": 1,
    "color": "red",
    "applicants": [
      {
          "id": 1
      },
      {
          "id": 2,
          "color": "blue"
      },
      {
          "id": 3
      }
    ]
  }
]
```

is effectively the same as this one:

```
[
  {
    "application_id": 1,
    "applicants": [
      {
          "id": 1,
          "color": "red"
      },
      {
          "id": 2,
          "color": "blue"
      },
      {
          "id": 3,
          "color": "red"
      }
    ]
  }
]
```



## Warnings

### Development

The server runs in development mode.  It has not been hardened for produciton-level
security or optimized for a production-level workload.

## TODOs

Check the project's issue tracker for features that will probably be required.