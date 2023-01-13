# Docker-compose nginx autossl
## Why
### - Easy http -> https for your website on docker-compose
### - Easy bind subdirectories and subdomains to your services
### - One configuration for multiple environments **[prod, staging, dev]**

## How
- Change docker-compose-example for your case
- Bind your services on subdomains and subdirectories in gateway-example.json
- Run `docker-compose up`


## Example
There's example configuration described in files docker-compose-example.yml and gateway-example.json

It makes services in docker-compose be available on next urls:
- https://api.staging.example.com — backend:8081
- https://staging.example.com/second_frontend/ — second-frontend:8080
- https://staging.example.com/ — frontend:8080

## Additional info
This repository based on https://github.com/Valian/docker-nginx-auto-ssl/
So you can use its documentation as additional information for use cases.

