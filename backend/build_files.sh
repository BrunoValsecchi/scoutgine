#!/bin/bash

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo "Running migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Build completed!"