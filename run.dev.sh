#!/bin/sh

docker-compose -f docker-compose.dev.yml --env-file env/.env.dev up --build