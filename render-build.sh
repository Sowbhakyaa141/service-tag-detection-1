#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Start the Flask app
gunicorn -b 0.0.0.0:$PORT app:app
