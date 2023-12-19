# `python-base` sets up all our shared environment variables
FROM python:3.8.1-slim as python-base

# Python environment variables
ENV PYTHONNONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Pip environment variables
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Paths
ENV PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Set up PATH to include necessary directories
ENV PATH="$VENV_PATH/bin:$PATH"

# Install dependencies for installing psycopg2 (PostgreSQL driver)
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Set the working directory
WORKDIR /app

# Copy the project files to the working directory
COPY . .

# Install runtime dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
