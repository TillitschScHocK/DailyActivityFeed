ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install requirements
RUN apk add --no-cache \
    python3 \
    py3-pip \
    tzdata

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY run.sh .

# Make executable
RUN chmod a+x /app/run.sh

# Expose port
EXPOSE 8099

CMD ["/app/run.sh"]
