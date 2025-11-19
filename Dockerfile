# ---------- Builder stage ----------
FROM python:3.11-bullseye AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Minimal build deps
RUN apt-get update --fix-missing && \
    apt-get -o Acquire::Retries=3 -o Acquire::ForceIPv4=true install -y --no-install-recommends \
      build-essential curl ca-certificates git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application source
COPY . /app

# Ensure entrypoint is present and executable in the builder stage
COPY entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh || true

# Bake NLTK data if needed
RUN python -m nltk.downloader punkt || true

# ---------- Runtime stage (slim) ----------
FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Create non-root user (still root while doing FS ops)
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

# Minimal runtime packages
RUN apt-get update --fix-missing && \
    apt-get -o Acquire::Retries=3 -o Acquire::ForceIPv4=true install -y --no-install-recommends \
      ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

# Copy pip-installed site-packages and app from builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Copy the entrypoint
COPY --from=builder /entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh || true

# Ensure ownership for runtime user
RUN chown -R appuser:appuser /app /entrypoint.sh || true

USER appuser
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]