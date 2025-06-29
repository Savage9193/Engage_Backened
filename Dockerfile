# Start with a slim Python image
FROM python:3.11-slim

# Install OS packages needed for Python and Rust builds
RUN apt-get update && apt-get install -y \
    curl build-essential gcc libffi-dev libpq-dev \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && rm -rf /var/lib/apt/lists/*

# Set Rust path
ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .
# Run migrations and collect static
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# Upgrade pip & install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (Render sets PORT automatically)
EXPOSE 8000

# Default command (for Django, use wsgi; for Flask, change it)
# CMD ["gunicorn", "engage_backend.wsgi:application", "--bind", "0.0.0.0:${PORT}"]
CMD gunicorn engage_backend.wsgi:application --bind 0.0.0.0:$PORT
