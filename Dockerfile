FROM python:3.11-slim

# System deps for Pillow, Tesseract, and PostgreSQL
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project (will be added after init)
COPY . .

# Entrypoint script handles migrations/collectstatic on container start
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command (dev server)
CMD ["gunicorn", "receipt_tracker.wsgi:application", "--bind", "0.0.0.0:8000"]
