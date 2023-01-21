#!/usr/bin/env bash
# Script to set up web server for deployment

sudo mkdir -p "/data/web_static/releases/test/" "/data/web_static/shared/"
echo "<h1>Hello World!</h1>" | sudo tee "/data/web_static/releases/test/index.html"
sudo ln -sf "/data/web_static/current" "/data/web_static/releases/test/"
sudo chown -hR ubuntu:ubuntu "/data/"


