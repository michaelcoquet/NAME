#!/bin/sh
cp /etc/letsencrypt/live/michaelcoquet.ca/fullchain.pem ssl/prod
cp /etc/letsencrypt/live/michaelcoquet.ca/privkey.pem ssl/prod

cp docker-compose.prod.yml docker-compose.yml
zip -r release.zip account common config dashboard db/01-init.sh env/.env.prod NAME spotify static scripts/entrypoints/prod ssl/prod Dockerfiles/prod docker-compose.yml manage.py requirements.txt

scp -i spotify_playground.pem release.zip ubuntu@ec2-35-169-165-156.compute-1.amazonaws.com:~/
rm -rf release.zip docker-compose.yml ssl/prod/fullchain.pem ssl/prod/privkey.pem