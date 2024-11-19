#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y $(cat packages.txt)

# Upgrade pip
python -m pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run Home.py --server.port 8501 --server.address 0.0.0.0