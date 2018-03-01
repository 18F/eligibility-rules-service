# Installing server locally

These instructions are to run a development 
copy of the rules server on our own machine, 
strictly for development purposes.
For directions on deploying to cloud.gov,
see [cloud.gov instructions](cloudgov.md).

## Clone repository 

First, you'll need to [install Git](https://gist.github.com/derhuerst/1b15ff4652a867391f03) and 
clone this repository.  Open a shell or terminal 
window, clone, and navigate to the directory 
containing the server code.

```
git clone https://github.com/18F/eligibility-rules-service.git
cd eligibility-rules-service
cd eligibility_rules_server
``` 

## Using Docker (recommended)

A Docker setup potentially makes development and deployment easier.

To use it, install [Docker][https://docs.docker.com/] 
and [Docker Compose][https://docs.docker.com/compose/install/]
if you haven't already.

Then run:

```
docker-compose up
```

The server should now be running; try using
http://localhost:8000/docs to try POSTing a 
request.


## Without Docker

1. Install PostgreSQL
1. Create a PostgreSQL superuser and a blank database: 
   `createuser --superuser admin; createdb -U admin eligibility`
1. Install [Pipenv](https://github.com/pypa/pipenv)
1. `pipenv install`
1. Set a `DATABASE_URL` environment variable, and verify that
   you can connect to the database: 
   `export DATABASE_URL=postgresql://admin:@/eligibility; 
   psql $DATABASE_URL`
1. `pipenv run manage.py migrate`
1. `pipenv run manage.py runserver 0.0.0.0:8000`

The server should now be running; try using
http://localhost:8000/docs to try POSTing a 
request.

