#!/bin/bash

# Start frontend
echo "Starting frontend..."
(cd ./frontend && npm run dev &) 

# Start backend
echo "Starting backend..."
(cd ./backend && gunicorn app:app &)