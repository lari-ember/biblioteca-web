#!/bin/bash

echo "Stopping and removing containers..."
docker-compose down

echo "Removing database volume..."
docker volume rm biblioteca-web_pgdata

echo "Rebuilding and restarting containers..."
docker-compose up --build
