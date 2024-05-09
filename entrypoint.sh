#!/bin/sh

# Check if the init has already been done
if [ ! -f "/app/.init_done" ]; then
    echo "Running init_data.py..."
    python init_data.py
    # Mark init as done
    echo "done" > /app/.init_done
fi

# Continue to the main process
exec "$@"