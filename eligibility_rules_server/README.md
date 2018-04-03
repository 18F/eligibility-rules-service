# eligibility-rules-server

A Django Rest Framework prototype implementation of the eligibility rules
service postulated at
[eligibility-rules-service](../README.md)

## Using the API

A sample server is running at https://eligibility-rules.app.cloud.gov/rulings/wic/federal/.

From the ["examples" directory](examples/README.md):

    curl -X POST -H "Content-Type: application/json" -d @wic-federal0.json https://eligibility-rules.app.cloud.gov/rulings/wic/federal/

If pipes are available (UNIX-like systems, including the
[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/about)),
you can prettify the output with Python or [jq](https://stedolan.github.io/jq/):

    curl -X POST -H "Content-Type: application/json" -d @wic-federal0.json https://eligibility-rules.app.cloud.gov/rulings/wic/federal/ | python -m json.tool

    curl -X POST -H "Content-Type: application/json" -d @wic-federal0.json https://eligibility-rules.app.cloud.gov/rulings/wic/federal/ | jq

## [Installation Instructions](installing.md)

[Installation instructions here](installing.md)

## [Deployment Instructions](cloudgov.md)

[Deployment instructions here](cloudgov.md)

## Technical info

- [Design notes](design.md)
- [Rule authoring guide](rules.md)

