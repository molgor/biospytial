#!/bin/bash
# This script stops the Biospytial Engine

##
echo "Stoping Biospytial services";
docker-compose -f container_files/biospytial_stack.yml -p biospytial down

echo "Ready, to start the engine run: ./startEngine.sh";



