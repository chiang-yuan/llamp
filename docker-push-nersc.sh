#!/bin/bash

docker build -t llamp-api-prod ./api
docker tag llamp-api-prod:latest registry.nersc.gov/matgen/llamp/llamp-api-prod:latest

docker build -t llamp-web-prod ./web
docker tag llamp-web-prod:latest registry.nersc.gov/matgen/llamp/llamp-web-prod:latest

docker push registry.nersc.gov/matgen/llamp/llamp-api-prod:latest
docker push registry.nersc.gov/matgen/llamp/llamp-web-prod:latest
