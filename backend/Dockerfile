FROM python:3.11-slim

WORKDIR /app

# Install system deps required for some python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps (docker-specific requirements)
COPY requirements-docker.txt ./
RUN python -m pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements-docker.txt

# Copy app
COPY . /app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
