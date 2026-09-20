# Multi-stage build: Python runtime
FROM python:3.11-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Final stage: Runtime image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    gosu \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (uid 10001)
RUN groupadd -r -g 10001 ecedocappuser && \
    useradd -r -u 10001 -g 10001 -m -d /app -s /sbin/nologin -c "Application user" ecedocappuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set PATH to use virtual environment
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Europe/Istanbul

# Copy application code
COPY --chown=ecedocappuser:ecedocappuser . /app/

# Create necessary directories with correct permissions
RUN mkdir -p /app/data /app/yemekfiles && \
    chown -R ecedocappuser:ecedocappuser /app/data /app/yemekfiles

# Copy and make entrypoint script executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 5003

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD python /app/healthcheck.py || exit 1

# Entry point
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command (gunicorn)
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5003", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "application:app"]
