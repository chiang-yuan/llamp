#!/bin/bash

docker build --no-cache -t llamp-api:test -f ./api/Dockerfile ./api
docker tag llamp-api:test registry.nersc.gov/matgen/llamp/llamp-api:test

docker build --no-cache -t llamp-web:test -f ./web/Dockerfile ./web
docker tag llamp-web:test registry.nersc.gov/matgen/llamp/llamp-web:test

docker push registry.nersc.gov/matgen/llamp/llamp-api:test
docker push registry.nersc.gov/matgen/llamp/llamp-web:test
