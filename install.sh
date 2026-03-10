#!/bin/bash

echo "Installing RY Music Bot..."

apt update -y
apt install python3 python3-pip git ffmpeg -y

pip3 install -r requirements.txt

echo "Install selesai"
