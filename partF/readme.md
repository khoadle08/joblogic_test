# Part F: Automated Log Rotation on Linux

This section presents a robust solution for automatically managing log files on a Linux server using a Bash script and `systemd` timers.

## Overview

The goal is to automatically archive and compress log files from the `/var/log/myapi/` directory that are older than 7 days. This helps save disk space and keeps the logging system tidy without losing historical data.

## Components

The solution consists of three main files:

1.  **`rotate_logs.sh`**: A Bash script that performs the core logic:
    * Finds `.log` files in `/var/log/myapi` older than 7 days.
    * Creates a single, timestamped `.tar.gz` archive containing all found log files.
    * Deletes the original log files after the archiving process is successful.
    * Logs key actions to the systemd journal for easy debugging.

2.  **`logrotate.service`**: A `systemd` unit file that defines a service to run the `rotate_logs.sh` script. It is configured to run once and then exit (`Type=oneshot`).

3.  **`logrotate.timer`**: A `systemd` timer file that triggers the `logrotate.service` on a defined schedule.
    * `OnCalendar=daily`: Runs the service once per day.
    * `Persistent=true`: If a run is missed (e.g., due to the server being off), it will be executed as soon as possible on the next boot.

## Installation Guide

To deploy this log rotation system on a Linux server (e.g., Ubuntu, CentOS), follow these steps with `sudo` privileges.

### 1. Copy the Script

Place the `rotate_logs.sh` script in a standard directory for local executables and make it executable.

```bash
# Place the script in /usr/local/bin
sudo cp rotate_logs.sh /usr/local/bin/rotate_logs.sh

# Make it executable
sudo chmod +x /usr/local/bin/rotate_logs.sh

2. Install the Systemd Files
Copy the .service and .timer files to the systemd configuration directory.

# Copy the service file
sudo cp logrotate.service /etc/systemd/system/logrotate.service

# Copy the timer file
sudo cp logrotate.timer /etc/systemd/system/logrotate.timer

3. Reload, Enable, and Start the Timer
Tell systemd to read the new configuration, then enable the timer to run on boot and start it immediately.

# Reload the systemd daemon
sudo systemctl daemon-reload

# Enable and start the timer
sudo systemctl enable --now logrotate.timer

Verification and Debugging
After installation, you can use the following commands to verify that everything is working correctly.

Check Timer Status
This command will show logrotate.timer in the list, along with its next scheduled run time.

systemctl list-timers

Run the Service Manually
To test the script immediately without waiting for the daily schedule:

sudo systemctl start logrotate.service

View Service Logs
Check the output from the last run of the service to see if it succeeded or encountered errors.

# View logs from the last run
journalctl -u logrotate.service

# Follow logs in real-time (useful for debugging)
journalctl -fu logrotate.service
