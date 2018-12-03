#!/usr/bin/env bash

# This file is to launch on docker celery and a flask server

# Start the celery worker in the background
celery worker -A tasks.celery --loglevel=info --concurrency=20 --detach

# Start the server
python server.py