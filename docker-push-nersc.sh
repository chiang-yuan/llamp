#!/bin/bash

docker build -t llamp-api-prod:test ./api
docker tag llamp-api-prod:test registry.nersc.gov/matgen/llamp/llamp-api-prod:test

docker build -t llamp-web-prod:test ./web
docker tag llamp-web-prod:test registry.nersc.gov/matgen/llamp/llamp-web-prod:test

docker push registry.nersc.gov/matgen/llamp/llamp-api-prod:test
docker push registry.nersc.gov/matgen/llamp/llamp-web-prod:test
