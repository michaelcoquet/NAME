#!/bin/sh
cp /etc/letsencrypt/live/michaelcoquet.ca/fullchain.pem ssl
cp /etc/letsencrypt/live/michaelcoquet.ca/privkey.pem ssl
cp docker-compose.prod.yml docker-compose.yml
zip -r release.zip account common config dashboard db env NAME ssl spotify static celery_entrypoint.sh docker-compose.yml Dockerfile.prod entrypoint.prod.sh flower_entrypoint.sh manage.py nginx_entrypoint.prod.sh requirements.txt
scp -i spotify_playground.pem release.zip ubuntu@ec2-35-169-165-156.compute-1.amazonaws.com:~/
rm -rf release.zip docker-compose.yml ssl/fullchain.pem ssl/privkey.pem