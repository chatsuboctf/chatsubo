#!/usr/bin/sh
set -euo pipefail

WORKER_TEMP_DIR=${WORKER_TEMP_DIR:-/dev/shm}
DB_URL=${CHATSUBO_DATABASE_URL:-}
WORKER_CLASS=${WORKER_CLASS:-eventlet}
ACCESS_LOG=${ACCESS_LOG:--}
ERROR_LOG=${ERROR_LOG:--}

# Check that the database is available
if [ -n "$DB_URL" ]
    then
    url=$(echo "$DB_URL" | awk -F[@//] '{print $4}')
    database=$(echo "$url" | awk -F[:] '{print $1}')
    port=$(echo "$url" | awk -F[:] '{print $2}')
    port=${port:=3306}
    echo "Waiting for $database:$port to be ready"
    while ! mysqladmin ping -h "$database" -P "$port" --silent; do
        # Show some progress
#        echo -n '.';
        sleep 1;
    done
    echo "$database is ready"
    # Give it another second.
    sleep 1;
fi

echo "Starting Chatsubo"
exec /opt/chatsubo/venv/bin/gunicorn app:server \
  --bind 0.0.0.0:8000 \
  --worker-class "$WORKER_CLASS" \
  --worker-tmp-dir "$WORKER_TEMP_DIR" \
  --workers 1 \
  --access-logfile "$ACCESS_LOG" \
  --error-logfile "$ERROR_LOG"
