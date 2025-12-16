#!/usr/bin/env bash
set -e

# Wait for DB (simple wait; replace with a robust check if needed)
echo "Waiting for database..."
sleep 3

# Run migrations if project exists
if [ -f "manage.py" ]; then
  echo "Running migrations..."
  python manage.py migrate || true
fi

exec "$@"
