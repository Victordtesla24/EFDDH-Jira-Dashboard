#!/bin/bash

# Create new directory structure
mkdir -p src/data/processors
mkdir -p src/services/jira
mkdir -p src/visualizations
mkdir -p src/utils
mkdir -p tests/{unit,integration,e2e}
mkdir -p .streamlit
mkdir -p assets/{css,images,templates}

# Move utility files to src/utils
mv utils/*.py src/utils/
rm -rf utils

# Move visualization files
mv src/utils/visualizations.py src/visualizations/
mv src/utils/metrics_calculator.py src/visualizations/

# Move data processing files
mv src/utils/data_processor.py src/data/processors/
mv src/utils/connection_manager.py src/services/jira/

# Move error handling and monitoring
mv src/utils/error_handler.py src/utils/
mv src/utils/health_monitor.py src/utils/
mv src/utils/logger.py src/utils/

# Create .streamlit config
cat > .streamlit/config.toml << EOL
[theme]
primaryColor = "#E694FF"
backgroundColor = "#00172B"
secondaryBackgroundColor = "#0083B8"
textColor = "#DCDCDC"
font = "sans-serif"

[server]
runOnSave = true
EOL

# Update imports in pages
for file in pages/*.py; do
    sed -i '' 's/from utils\./from src.utils./g' "$file"
    sed -i '' 's/from visualizations/from src.visualizations/g' "$file"
    sed -i '' 's/from data_processor/from src.data.processors.data_processor/g' "$file"
done

# Update Home.py imports
sed -i '' 's/from utils\./from src.utils./g' Home.py
sed -i '' 's/from visualizations/from src.visualizations/g' Home.py
sed -i '' 's/from data_processor/from src.data.processors.data_processor/g' Home.py

# Create __init__.py files
touch src/__init__.py
touch src/data/__init__.py
touch src/data/processors/__init__.py
touch src/services/__init__.py
touch src/services/jira/__init__.py
touch src/visualizations/__init__.py
touch src/utils/__init__.py

# Update pyproject.toml
cat > pyproject.toml << EOL
[tool.poetry]
name = "efddh-dashboard"
version = "0.1.0"
description = "EFDDH Jira Dashboard"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
streamlit = "^1.31.0"
pandas = "^2.0.0"
plotly = "^5.18.0"

[tool.mypy]
python_version = "3.9"
strict = true
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = [
    "streamlit.*",
    "pandas.*",
    "plotly.*"
]
ignore_missing_imports = true

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
EOL

# Clean up __pycache__ directories
find . -type d -name "__pycache__" -exec rm -r {} +