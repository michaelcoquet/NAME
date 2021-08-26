#!/bin/sh

echo "starting nginx"
# hardcoding the nginx configuration file to hide the proxy address
# and port
echo "server {
    listen 80;
    server_name spotify.michaelcoquet.ca;

    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

server {
    listen                443 ssl;
    server_name           spotify.michaelcoquet.ca;
    ssl_certificate       /etc/nginx/ssl/prod/fullchain.pem;
    ssl_certificate_key   /etc/nginx/ssl/prod/privkey.pem;
    ssl_protocols         TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers           HIGH:!aNULL:!MD5;
    access_log            /var/log/nginx/access.log;
    error_log             /var/log/nginx/nginx_error.log;
    
    location / {
        proxy_pass                         https://${PROXY_SOCK};
        proxy_set_header X-Forwarded-For   \$proxy_add_x_forwarded_for;
        proxy_set_header Host              \$host;
        proxy_redirect                     off;    
    }

    location /static/css {
        types{
            text/css css;
        }
        alias /static/css;
    }

    location /static/img {
        types{
            image/png png;
            image/webp webp;
        }
        alias /static/img;
    }
    
    location /static/admin {
        alias /static/admin;
    }

    location /static/django_extensions {
        alias /static/django_extensions;
    }
}" > ./config/nginx.conf
cp ./config/default-nginx.conf ./etc/nginx/nginx.conf
mkdir -p ./etc/nginx/ssl/prod
cp ./ssl/prod/fullchain.pem ./etc/nginx/ssl/prod/fullchain.pem
cp ./ssl/prod/privkey.pem ./etc/nginx/ssl/prod/privkey.pem
chmod 775 -R ./static 
nginx -g 'daemon off;'
sleep infinity
