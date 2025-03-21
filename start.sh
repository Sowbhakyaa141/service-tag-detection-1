#!/bin/bash

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Start the Flask app
gunicorn -b 0.0.0.0:$PORT app:app

apt-get update && apt-get install -y libgl1-mesa-glx
