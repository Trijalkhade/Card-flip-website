#!/bin/sh
# wait-for-postgres.sh
set -e

host="$1"
shift

until pg_isready -h "$host" -U postgres > /dev/null 2>&1; do
  >&2 echo "⏳ Waiting for Postgres at $host..."
  sleep 2
done

>&2 echo "✅ Postgres is up - executing command"
exec "$@"
