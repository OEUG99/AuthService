# Authentication Service & Main Service:
This is the primary service for the dating app. It is responsible for all of the user authentication and user data. 

In this repo we have the following:
* User Authentication Service:
* * This service is responsible for all of the user authentication. It is a RESTful API that is used by the main service to authenticate users.
* * It is written in Python using the Flask framework.
* * It has hotswap-able database support at runtime thanks to using our [database abstraction layer](https://en.wikipedia.org/wiki/Database_abstraction_layer).
* Consul Service Discovery:
* * This service has a container for consul that is used for service discovery.
* Scripts for manging the service:
* * `docker-compose.yml`
* * * This file is used to start the service.
* * * It is used by the [docker-compose](https://docs.docker.com/compose/) command.
* * `/scripts/generate_ngninx_config.py` 
* * * This script communicates with consul to get a list of services and then generates a nginx configuration file that will proxy to those services.
* * * It creates a nginx configuration file that will proxy to the user authentication service.
* * * This script is similar to how consul templates work if you are familiar with them.
* * * This allows nginx to act as an aggregation layer!
* * * It is used by the `update_nginx_config.sh` script.
* * `/scripts/update_nginx_config.sh`
* * * This script will update the nginx configuration file and then reload nginx.

## Environment Variables:
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_SESSION_TOKEN
* AWS_SECRET_KEY_NAME
* AWS_REGION
* AWS_OUTPUT
* GIT_TOKEN
* MYSQL_ROOT_PASSWORD
* MYSQL_DATABASE
* MYSQL_USER
* MYSQL_PASSWORD
* REDIS_PASSWORD
* CONSUL_IP
* SERVICE_PORT
* SERVICE_IP

## Usage:
* `docker-compose up -d`
* * This will start the service.
* `docker-compose down`
* * This will stop the service.
* `docker-compose logs -f`
* * This will show the logs for the service.
* `python service_registry.py` when connected to the container to register with consul (this will be automated in future)

## Useful Commands:
* list of useful commands can be found in the scripts folder.

## Requirements:
* Docker
* Docker Compose
* Python 3.6
* nginx 
* aws cli & account for secret management (will be optional in future)
* Access to the PyDataOpsKit repo (currently private but will be public once initial development is complete, contact me for early access)
