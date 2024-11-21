#!/bin/bash

# Fix trailing whitespace
find . -type f -name "*.py" -exec sed -i '' -e 's/[[:space:]]*$//' {} +

# Ensure files end with newline
find . -type f -name "*.py" -exec sh -c '
  if [ -n "$(tail -c1 "$1")" ]; then
    echo "" >> "$1"
  fi
' sh {} \;
