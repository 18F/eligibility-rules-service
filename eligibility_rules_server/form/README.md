# eligibility-rules-server form

A React static form to make example requests from the [eligibility-rules-service](../README.md). Static
site generation built with [Gatsbyjs](https://www.gatsbyjs.org/)

## Development Instructions

- Run `docker-compose up`
- The `form` service will install packages and launch the development server.
- Once the server is up, navigate to [http://localhost:9000](http://localhost:9000)

## Building the Static Site

- Run `docker-compose run form yarn build`
- Static assets will be placed into the `public/` folder
