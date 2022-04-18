#!/bin/sh

ENV_FILE=$1
export REDIS_HOST=$(grep REDIS_HOST $ENV_FILE | cut -d '=' -f2)
export REDIS_PORT=$(grep REDIS_PORT $ENV_FILE | cut -d '=' -f2)
export DEBUG=$(grep DEBUG $ENV_FILE | cut -d '=' -f2)

#host = "172.17.0.1" # "redis-service" # "redisearch-service"
echo main.py REDIS_HOST=$REDIS_HOST REDIS_PORT=$REDIS_PORT DEBUG=$DEBUG
#python3 main.py REDIS_HOST=$REDIS_HOST REDIS_PORT=$REDIS_PORT DEBUG=$DEBUG
waitress-serve --port=5973 --call main:create_app
