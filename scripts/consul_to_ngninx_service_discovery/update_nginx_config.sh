#!/bin/bash
# run as root.
# This script will refresh nginx configuration
# and restart nginx service

# Fetching confing from config directory:
NGINX_CONF=$(dirname $(pwd))/scripts/ngnix_dev.conf

# Kill nginx process:
killall nginx

# update config:
nginx -t -c $NGINX_CONF

# start nginx:
nginx -c $NGINX_CONF
