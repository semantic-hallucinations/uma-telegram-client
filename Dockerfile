FROM python:3.10-slim

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ src/

RUN mkdir -p src/logs


CMD ["python", "src/main.py"]