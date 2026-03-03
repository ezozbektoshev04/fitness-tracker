# =======================
# STAGE 1: Builder
# =======================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --target=/app/packages

# =======================
# STAGE 2: Production
# =======================
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy packages from builder
COPY --from=builder /app/packages /app/packages

# Add packages to Python path
ENV PYTHONPATH=/app/packages
ENV PATH=/app/packages/bin:$PATH

# Create non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Copy project files
COPY . .

# Create directories and set permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["python", "-m", "gunicorn", "core.wsgi:application", "--config", "gunicorn.conf.py"]
