#!/bin/bash

TODAY=$(date +%Y-%m-%d)
FLAG_FILE="/home/mat/Documents/blogg/.ran_today_$TODAY"
FLAG_DIR="/home/mat/Documents/blogg"
cd $FLAG_DIR

# force thing
FORCE_RUN=false
if [ "$1" == "--force" ] || [ "$1" == "-f" ]; then
  FORCE_RUN=true
fi


# Clean up old flag files (keep only last 7 days for safety)
find "$FLAG_DIR" -name ".ran_today_*" -type f -mtime +7 -delete

# Check if already run today, unless force flag is used
if [ -f "$FLAG_FILE" ] && [ "$FORCE_RUN" = false ]; then
  echo "Already ran today, exiting. Use --force to run anyway." >> "$FLAG_DIR"/poem_cron.log
  exit 0
fi

# # # do the dirty work boi; this is the original script (all grown up)
source .venv/bin/activate
$FLAG_DIR/daily_poem.py

# Create flag file after successful completion
touch "$FLAG_FILE"
