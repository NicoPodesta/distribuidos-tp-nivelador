#!/usr/bin/env bash

NETWORK_NAME="tp-nivelador_default"
SERVER_HOST="server"
SERVER_PORT=5678
MESSAGE="Hello World"

echo "Connecting to the server via $NETWORK_NAME..."

echo "Response received: $(docker run --rm --network "$NETWORK_NAME" busybox sh -c "echo -n '$MESSAGE' | timeout 1 nc $SERVER_HOST $SERVER_PORT")"
