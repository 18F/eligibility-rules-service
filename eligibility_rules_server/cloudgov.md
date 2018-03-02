# Deployment 

## Warning

The codebase as-written has only a 
development form.  Before deploying in 
production, the configuration should be 
hardened.

## Cloud.gov 

To deploy the application to cloud.gov, or to similar
[CloudFoundry](https://www.cloudfoundry.org/)-based providers:

1. Follow [cloud.gov instructions](https://cloud.gov/docs/)
to set up a cloud.gov account, install the 
`cf` application to your machine, and login.

2. Create a database service:

    cf create-service aws-rds shared-psql eligibility-db 
   
3. From the `eligibility-rules-service/eligibility_rules_server`
   directory, issue `cf push`  

