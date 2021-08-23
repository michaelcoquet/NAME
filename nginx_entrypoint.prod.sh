#!/bin/sh

echo "starting nginx"
cp ./config/default-nginx.conf ./etc/nginx/nginx.conf
chmod 775 -R ./static 
nginx -g 'daemon off;'
sleep infinity