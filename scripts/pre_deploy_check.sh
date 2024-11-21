#!/bin/bash
set -e

echo "Running pre-deployment checks..."

# Run tests
echo "Running tests..."
pytest -v

# Run linters
echo "Running linters..."
black . --check
isort . --check
flake8

# Check dependencies
echo "Checking dependencies..."
pip check

# Run type checking
echo "Running type checking..."
mypy src/

# Verify Streamlit app
echo "Verifying Streamlit app..."
streamlit run Home.py --headless --browser.serverAddress localhost &
PID=$!
sleep 5
kill $PID

echo "All checks passed! Ready for deployment."
