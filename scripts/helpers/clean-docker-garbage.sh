#!/bin/sh

docker system prune --all --volumes --force
systemctl stop docker
rm -rf var/lib/docker
systemctl start docker