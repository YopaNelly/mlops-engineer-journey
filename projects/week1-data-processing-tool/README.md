# Week 1 — ML Data Processing Automation Tool

## Problem

Raw data coming from real-world sources is rarely clean. Rows go missing
critical values, numbers get stored as text with symbols like $ mixed in,
and duplicate rows sneak in from repeated imports. Feeding this straight
into a model produces unreliable results without any warning that
something was wrong. This tool cleans and validates data automatically,
and just as importantly logs exactly what it changed and why.

## Architecture

Raw CSV
   |
   v
handle_missing()   -> drops rows missing required fields, logs how many
   |
   v
dedupe()           -> removes exact duplicate rows, logs how many
   |
   v
fix_types()        -> converts numeric columns, logs any conversion failures
   |
   v
Cleaned CSV + full log trail

Config (configs/config.yaml) controls which columns are required and
which are numeric — nothing is hardcoded, so this tool works on a new
dataset just by changing the config.

## How to run

poetry install
poetry run python -m my_tool --input path/to/data.csv --config configs/config.yaml --output cleaned.csv

## Lessons learned

The most important lesson from this week wasn't the cleaning logic itself,
it was realizing that a cleaning step which "succeeds" without complaint
can still silently destroy data, converting a price with an unexpected
symbol into NaN for every row, for example. Comparing valid-value counts
before and after each transformation, and logging loudly the moment
something looks wrong, turned a category of bug that could take hours to
notice into one that shows up in the log on the very first run.
