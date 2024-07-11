#!/bin/bash
echo "Starting application..."
./build/telegram-bot-api --local --api-id=$API_ID --api-hash=$API_HASH --dir=/data/telegram-api --http-port=8080
