#!/bin/bash

TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
FLAG_FILE="/home/mat/Documents/blogg/.ran_today_$TODAY"
FLAG_DIR="/home/mat/Documents/blogg"
LOG_FILE="$FLAG_DIR/poem_cron.log"
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
  echo "[$TIMESTAMP] Already ran today, exiting. Use --force to run anyway." >> "$LOG_FILE"
  exit 0
fi

echo "[$TIMESTAMP] Starting daily poem run" >> "$LOG_FILE"

# # # do the dirty work boi; this is the original script (all grown up)
source .venv/bin/activate
if ! $FLAG_DIR/daily_poem.py >> "$LOG_FILE" 2>&1; then
  echo "[$TIMESTAMP] ERROR: daily_poem.py failed with exit code $?" >> "$LOG_FILE"
  exit 1
fi

echo "[$TIMESTAMP] Successfully completed daily poem run" >> "$LOG_FILE"

# Create flag file after successful completion
touch "$FLAG_FILE"
