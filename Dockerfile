FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --target=/app/packages

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/packages /app/packages

ENV PYTHONPATH=/app/packages
ENV PATH=/app/packages/bin:$PATH

# Create non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

COPY . .

RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["python", "-m", "gunicorn", "core.wsgi:application", "--config", "gunicorn.conf.py"]
