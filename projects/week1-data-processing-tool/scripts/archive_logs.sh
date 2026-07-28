#!/bin/bash
set -e

cd "$(dirname "$0")/.."

LOG_DIR="logs"
ARCHIVE_DIR="logs/archive"

echo "Checking for log files older than 7 days in $LOG_DIR..."

# Make sure the archive folder exists
mkdir -p "$ARCHIVE_DIR"

# Find files in LOG_DIR (not in subfolders) older than 7 days, and move each one
find "$LOG_DIR" -maxdepth 1 -name "*.log*" -mtime +7 -print | while read -r file; do
    echo "Archiving: $file"
    mv "$file" "$ARCHIVE_DIR/"
done

echo "Archiving complete."
