#!/bin/sh

echo "starting nginx"
cp ./config/default-nginx.conf ./etc/nginx/nginx.conf
mkdir -p ./etc/nginx/ssl
cp ./ssl/fullchain.pem ./etc/nginx/ssl/fullchain.pem
cp ./ssl/privkey.pem ./etc/nginx/ssl/privkey.pem
# cp ssl/dev.crt ./etc/nginx/ssl/dev.crt
# cp ssl/dev.key ./etc/nginx/ssl/dev.key
chmod 775 -R ./static 
nginx -g 'daemon off;'
sleep infinity
