#!/bin/bash

# Start dbus service
service dbus start

# Print message to confirm script execution
echo "Starting Flask app and Chromium..."

# Start Flask app in the background
python /app/API/API/app.py &

# Start Chromium in headless mode via xvfb-run
xvfb-run --server-args='-screen 0 1280x1024x24' chromium --headless --disable-gpu --no-sandbox --remote-debugging-port=9222 &

# Wait for both processes to ensure they stay running
wait
