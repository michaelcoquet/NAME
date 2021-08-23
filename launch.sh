#!/bin/sh
cp docker-compose.prod.yml docker-compose.yml
zip -r release.zip account common config dashboard db env NAME spotify static celery_entrypoint.sh docker-compose.yml Dockerfile.prod entrypoint.prod.sh flower_entrypoint.sh manage.py nginx_entrypoint.prod.sh init-letsencrypt.sh requirements.txt
scp -i spotify_playground.pem release.zip ubuntu@ec2-35-169-165-156.compute-1.amazonaws.com:~/
rm -rf release.zip docker-compose.yml