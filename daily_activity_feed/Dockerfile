FROM python:3.11-alpine

WORKDIR /app

# Install dependencies
RUN apk add --no-cache tzdata

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY run.sh .

# Make run script executable
RUN chmod +x /app/run.sh

# Expose port
EXPOSE 8099

# Run the application
CMD ["/app/run.sh"]