#!/bin/bash

# Activate your virtual environment if necessary
SOURCE_PATH=".venv/bin/activate"
source $SOURCE_PATH

sleep 1

# Start the FastAPI app using uvicorn
uvicorn main:zaloapp --reload --env-file .env --host 0.0.0.0 --port 9090 