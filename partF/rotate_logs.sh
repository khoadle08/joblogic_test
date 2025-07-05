#!/bin/bash

# ==============================================================================
# rotate_logs.sh
#
# This script finds, archives, compresses, and deletes old log files.
# ==============================================================================

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
LOG_DIR="/var/log/myapi"
ARCHIVE_DIR="/var/log/myapi/archives"
RETENTION_DAYS=7

# --- Logic ---

# 1. Check if the log directory exists
if [ ! -d "$LOG_DIR" ]; then
  echo "Log directory not found: $LOG_DIR"
  # Log to systemd journal instead of echo
  /usr/bin/logger "Log rotation failed: Directory $LOG_DIR not found."
  exit 1
fi

# 2. Create the archive directory if it doesn't exist
mkdir -p "$ARCHIVE_DIR"

# 3. Find log files older than RETENTION_DAYS
# Use 'find' to locate files and store them in an array.
# '-mtime +$((RETENTION_DAYS - 1))' is equivalent to "older than 7 days".
files_to_archive=()
while IFS= read -r -d $'\0'; do
    files_to_archive+=("$REPLY")
done < <(find "$LOG_DIR" -maxdepth 1 -type f -name "*.log" -mtime +"$((RETENTION_DAYS - 1))" -print0)

# 4. If there are no files to archive, exit
if [ ${#files_to_archive[@]} -eq 0 ]; then
  echo "No log files older than $RETENTION_DAYS days to archive."
  /usr/bin/logger "Log rotation: No old log files to archive."
  exit 0
fi

# 5. Create a timestamped archive file
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
ARCHIVE_FILE="$ARCHIVE_DIR/logs-archive-${TIMESTAMP}.tar.gz"

echo "Archiving ${#files_to_archive[@]} files to ${ARCHIVE_FILE}..."
/usr/bin/logger "Archiving ${#files_to_archive[@]} log files to ${ARCHIVE_FILE}."

# Create the archive and delete the original files on success
# 'tar' will work with the absolute paths of the found files
if tar -czf "$ARCHIVE_FILE" "${files_to_archive[@]}"; then
  echo "Archive successful. Removing original log files..."
  rm -f "${files_to_archive[@]}"
  /usr/bin/logger "Log rotation successful. Removed original files."
else
  echo "Error: Could not create archive file."
  /usr/bin/logger "Log rotation failed: Could not create archive file."
  exit 1
fi

echo "Complete."
exit 0
