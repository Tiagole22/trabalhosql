FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_MODULE=frontend:app

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8080} ${APP_MODULE}"]
