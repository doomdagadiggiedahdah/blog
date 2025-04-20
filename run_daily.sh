#!/bin/bash

TODAY=$(date +%Y-%m-%d)
FLAG_FILE="/home/mat/Documents/blogg/.ran_today_$TODAY"
FLAG_DIR="/home/mat/Documents/blogg"
cd $FLAG_DIR

# Clean up old flag files (keep only last 7 days for safety)
find "$FLAG_DIR" -name ".ran_today_*" -type f -mtime +7 -delete

if [ -f "$FLAG_FILE" ]; then
  echo "Already ran today, exiting" >> "$FLAG_DIR"/poem_cron.log
  exit 0
fi

# # # do the dirty work boi; this is the original script (all grown up)
source .venv/bin/activate
$FLAG_DIR/daily_poem.py

# Create flag file after successful completion
touch "$FLAG_FILE"
