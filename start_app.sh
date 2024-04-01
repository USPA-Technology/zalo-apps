#!/bin/bash

DIR_PATH="."

# Change to the directory where your FastAPI app is located

if [ -d "$DIR_PATH" ]; then
  cd $DIR_PATH
fi

# kill old process to restart
kill -15 $(pgrep -f "uvicorn main:zaloapp")
sleep 2

# Activate your virtual environment if necessary
SOURCE_PATH=".venv/bin/activate"
source $SOURCE_PATH

# clear old log
# cat /dev/null > zaloapp.log
datetoday=$(date '+%Y-%m-%d')
log_file="zaloapp-$datetoday.log"


# Start the FastAPI app using uvicorn
uvicorn main:zaloapp --reload --env-file .env --host 0.0.0.0 --port 9090 >> $log_file 2>&1 &

# exit
deactivate