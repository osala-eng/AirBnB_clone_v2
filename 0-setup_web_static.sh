#!/usr/bin/env bash
# Script to set up web server for deployment

mkdir -p "/data/web_static/releases/test/"
mkdir -p "/data/web_static/shared/"
ln -s "/data/web_static/current" "/data/web_static/releases/test/"
