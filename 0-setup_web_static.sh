#!/usr/bin/env bash
# Script to set up web server for deployment

mkdir -p "/data/web_static/releases/test/"
mkdir -p "/data/web_static/shared/"
echo "<h1>Hello World!</h1>" > "/data/web_static/releases/test/index.html"
ln -sf "/data/web_static/current" "/data/web_static/releases/test/"
chown -R ubuntu:ubuntu "/data/"
