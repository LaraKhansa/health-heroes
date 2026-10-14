FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    DATABASE_URL=sqlite:////app/data/health_heroes.db \
    PORT=8000

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data && useradd --create-home appuser && chown -R appuser /app
USER appuser

VOLUME ["/app/data"]
EXPOSE 8000

# --preload creates and seeds the database once before workers start
CMD gunicorn --preload --workers 2 --timeout 120 --bind 0.0.0.0:${PORT} main:app
