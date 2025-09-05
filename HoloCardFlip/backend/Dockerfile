FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies (needed for psycopg2 and postgres client)
RUN apt-get update && apt-get install -y gcc libpq-dev postgresql-client && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy wait-for-postgres script and make it executable
COPY wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

EXPOSE 8000

# Use wait-for-postgres to ensure DB is ready before starting FastAPI
CMD ["./wait-for-postgres.sh", "postgres", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
