#!/bin/bash

# 1. Force the script to run from the folder where the file is located
#    This fixes the "Empty Data" issue.
cd "$(dirname "$0")"

# 2. Kill any old background instances of the server (cleans up port 8000)
lsof -ti:8000 | xargs kill -9 >/dev/null 2>&1

# 3. Start the server in the background
echo "Starting SkiLuxe Server..."
python3 server.py &

# 4. Wait 2 seconds to ensure the server is ready (Fixes connection errors)
sleep 2

# 5. Open the browser
open "http://localhost:8000"

# 6. Keep the Terminal window open so the server keeps running
wait