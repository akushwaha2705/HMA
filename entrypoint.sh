#!/usr/bin/env bash
set -euo pipefail
# Entrypoint for fsai container
# - Waits for DB (optional)
# - Runs migrations (fails fast on error)
# - Runs collectstatic
# - Mandatory: runs /app/create_users.py (container exits if it fails or is missing)
# - Starts gunicorn

log() {
  # timestamped log to stdout
  printf '%s %s\n' "$(date --iso-8601=seconds 2>/dev/null || date)" "$*"
}

wait_for_db() {
  if [ -n "${DB_HOST:-}" ]; then
    local timeout=${DB_WAIT_SECS:-60}
    local elapsed=0
    log "Waiting for DB ${DB_HOST}:${DB_PORT:-5432} (timeout ${timeout}s)..."

    # prefer nc if available
    if command -v nc >/dev/null 2>&1; then
      while [ $elapsed -lt $timeout ]; do
        if nc -z "${DB_HOST}" "${DB_PORT:-5432}"; then
          log "DB reachable (nc)."
          return 0
        fi
        sleep 2
        elapsed=$((elapsed+2))
      done
    else
      # fallback: try python socket connect
      while [ $elapsed -lt $timeout ]; do
        python - <<PY 2>/dev/null || true
import socket, os, sys
s = socket.socket()
try:
    s.settimeout(1.0)
    s.connect((os.getenv('DB_HOST'), int(os.getenv('DB_PORT','5432'))))
    print("OK")
except Exception:
    sys.exit(1)
finally:
    s.close()
PY
        if [ $? -eq 0 ]; then
          log "DB reachable (python)."
          return 0
        fi
        sleep 2
        elapsed=$((elapsed+2))
      done
    fi

    log "Timed out waiting for DB after ${timeout}s."
    return 1
  fi

  log "DB_HOST not set; skipping DB wait."
  return 0
}

main() {
  log "Entrypoint started"

  # Wait for DB (but do not continue blindly if unreachable)
  if ! wait_for_db; then
    log "ERROR: Database did not become ready in time. Exiting."
    exit 1
  fi

  # Run migrations (fail fast if migrations error)
  log "Applying migrations..."
  if ! python manage.py migrate --noinput; then
    log "ERROR: migrations failed. Exiting."
    exit 1
  fi
  log "Migrations applied successfully."

  # Collect static files
  log "Collecting static files..."
  if ! python manage.py collectstatic --noinput; then
    log "ERROR: collectstatic failed. Exiting."
    exit 1
  fi
  log "Collectstatic completed."

  # Mandatory: create initial users (must be present and succeed)
  log "MANDATORY: creating initial users from /app/create_users.py"

  if [ -f "/app/create_users.py" ]; then
    python manage.py shell < /app/create_users.py
    rc=$?

    if [ $rc -ne 0 ]; then
      log "ERROR: Mandatory create_users.py failed with exit code $rc — aborting container startup."
      exit $rc
    else
      log "OK: create_users.py ran successfully."
    fi
  else
    log "ERROR: /app/create_users.py not found — aborting container startup."
    exit 2
  fi

  # Start Gunicorn as PID 1 (so signals are forwarded)
  log "Starting Gunicorn..."
  exec gunicorn hma.wsgi --bind 0.0.0.0:8000 --timeout 120
}

# Run the main function
main "$@"