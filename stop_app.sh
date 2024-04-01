#!/bin/sh

kill -15 $(pgrep -f "uvicorn main:zaloapp")
sleep 2