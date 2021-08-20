#!/bin/sh

echo "starting nginx"
mkdir -p ./etc/nginx/ssl
cp ./config/default-nginx.conf ./etc/nginx/nginx.prod.conf
cp ssl/name.crt ./etc/nginx/ssl/name.crt
cp ssl/name.key ./etc/nginx/ssl/name.key
chmod 775 -R ./static 
nginx -g 'daemon off;'
sleep infinity