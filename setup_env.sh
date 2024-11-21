# Cleaning Project before Testing
# Clean and remove test cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
rm -rf .pytest_cache .coverage .mypy_cache
rm -rf .git/hooks/pre-commit
rm -rf ~/.cache/pre-commit
pre-commit uninstall
pre-commit install
# Remove current VM and Rebuild with Requirements.txt
rm -rf venv
python3.13 -m venv venv || error "Failed to create virtual environment"
source venv/bin/activate || error "Failed to activate virtual environment"
pip install --upgrade pip
pip install -r requirements.txt
pip install pre-commit black isort flake8 flake8-docstrings pytest pytest-cov
# Setup Configs
pre-commit uninstall
pre-commit install

# Run Tests
pytest -v tests/
