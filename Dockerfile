
# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"

# Set work directory
WORKDIR /app

# Install system dependencies (optional but often needed)
RUN apt-get update \
  && apt-get install -y build-essential libpq-dev curl \
  && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the port Render will assign
EXPOSE 8000

# This ensures your uploaded files are included in the Docker image
RUN mkdir -p /app/media
COPY ./media /app/media

# Run migrations + start server when container starts (not during build)
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn engage_backend.wsgi:application --bind 0.0.0.0:$PORT"]
