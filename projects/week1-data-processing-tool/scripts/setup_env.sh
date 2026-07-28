#!/bin/bash
set -e

echo "Setting up week1-data-processing-tool..."

# Go to the project root (one level up from scripts/)
cd "$(dirname "$0")/.."

# Install all dependencies exactly as locked in poetry.lock
echo "Installing dependencies with Poetry..."
poetry install

# Make sure the logs folder exists (logger.py expects it)
echo "Creating logs directory if missing..."
mkdir -p logs

# Run a quick sanity check that the project actually works
echo "Running sanity check..."
poetry run python src/main.py

echo "Setup complete. Project is ready to use."
