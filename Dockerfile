# --- STAGE 1: Build Frontend ---
FROM node:18 AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# --- STAGE 2: Flask Backend mit integriertem Frontend ---
FROM python:3.10-slim

# System-Dependencies für psycopg2 etc.
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Backend-Code
COPY backend /app/backend
COPY reports /app/reports
COPY backend/app.py /app/app.py

# Statisches Frontend (aus Build)
COPY --from=frontend-builder /app/frontend/build /app/frontend_build

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

EXPOSE 5000
ENV PYTHONUNBUFFERED=1
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
