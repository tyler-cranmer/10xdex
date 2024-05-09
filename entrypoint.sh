#!/bin/sh

# Path to a file that flags whether initialization has been done
INIT_DONE="/app/init_done.flag"

wait_for_db() {
    echo "Waiting for TimescaleDB to be ready..."
    local retries=30
    while ! pg_isready -h timescaledb -p 5432 > /dev/null 2> /dev/null; do
        retries=$((retries - 1))
        if [ $retries -le 0 ]; then
            echo "TimescaleDB did not become ready in time."
            return 1
        fi
        sleep 1
    done
    echo "TimescaleDB is ready!"
}
# Check if the initialization has already been done
if [ ! -f "$INIT_DONE" ]; then
    # Wait for TimescaleDB to be ready
    wait_for_db

    echo "Running Alembic upgrades..."
    # Run Alembic migrations to set up or update the database schema
    alembic upgrade head

    echo "Running init_data.py..."
    # Populate data
    python /app/init_data.py
    echo "Data initialization complete."

    # Mark init as done by creating a flag file
    touch $INIT_DONE
else
    echo "Initialization already done."
fi

# Continue to the main process
exec "$@"
