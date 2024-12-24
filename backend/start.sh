# start.sh
#!/bin/bash

# Start Chromium in the background
/usr/bin/chromium --headless --no-sandbox --disable-dev-shm-usage --remote-debugging-port=9222 &

# Start the Flask app
python /app/API/app.py
