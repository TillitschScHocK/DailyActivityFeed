#!/usr/bin/with-contenv bashio

# Get configuration
PORT=$(bashio::config 'port')

# Export for Python app
export PORT=${PORT}

# Start the application
bashio::log.info "Starting Daily Activity Feed on port ${PORT}"
python3 /app/app.py