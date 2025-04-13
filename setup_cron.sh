#!/bin/bash

# Configuration - Edit these variables to customize
SCRIPT_DIR="/home/mat/Documents/blog"
SCRIPT_NAME="daily_poem.py"
CRON_TIME="0 8 * * *"  # Run at 8:00 AM daily
LOG_FILE="poem_cron.log"

# Full path to the script
SCRIPT_PATH="${SCRIPT_DIR}/${SCRIPT_NAME}"

# Verify the script exists
if [ ! -f "$SCRIPT_PATH" ]; then
  echo "Error: Script not found at $SCRIPT_PATH"
  exit 1
fi

# Ensure script is executable
chmod +x "$SCRIPT_PATH"

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_TIME cd $SCRIPT_DIR && ./$SCRIPT_NAME >> $LOG_FILE 2>&1") | crontab -

echo "Cron job set up to run at: $CRON_TIME"
echo "The script will run from: $SCRIPT_DIR"
echo "Logs will be written to: $SCRIPT_DIR/$LOG_FILE"
echo "To verify, run: crontab -l"
echo "The script will use the ANTHROPIC_API_KEY from your environment."