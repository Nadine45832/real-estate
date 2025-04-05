#!/bin/bash

# Kill background processes on script exit
trap 'kill $(jobs -p)' EXIT

# Start frontend
echo "Starting frontend..."
(cd ./frontend && npm run dev) & 

# Start backend
echo "Starting backend..."
(cd ./backend && gunicorn app:app) &

# Wait for all background jobs
wait