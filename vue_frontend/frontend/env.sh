#!/usr/bin/env bash
set -eu

echo "
server {
  listen ${NGINX_PORT};
  
  location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
    include /etc/nginx/mime.types;
    try_files \$uri \$uri/ /index.html =404;
  }

  location /api/v1/ {
   proxy_pass ${NGINX_PROXY_PASS};
  }
  
  include /etc/nginx/extra-conf.d/*.conf;


}" > /etc/nginx/conf.d/default.conf
