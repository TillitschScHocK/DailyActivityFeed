#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "------------------------------------------"
bashio::log.info "Starting Daily Activity Feed..."
bashio::log.info "------------------------------------------"

# Get configuration from options
PORT=$(bashio::config 'port')
MAX_EVENTS=$(bashio::config 'max_events_per_day')

bashio::log.info "Configuration:"
bashio::log.info "  Port: ${PORT}"
bashio::log.info "  Max events per day: ${MAX_EVENTS}"

# Export for Python app
export PORT=${PORT}
export MAX_EVENTS=${MAX_EVENTS}

bashio::log.info "------------------------------------------"
bashio::log.info "Launching API server..."
bashio::log.info "Listening on: http://0.0.0.0:${PORT}"
bashio::log.info "------------------------------------------"

# Start the application
python3 /app/app.py
