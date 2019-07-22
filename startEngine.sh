#!/bin/bash
# This script starts the Biospytial Engine

##
echo "Starting Biospytial services";
docker-compose -f container_files/biospytial_stack.yml -p biospytial up -d;

echo "Ready, to stop the engine run: ./stopEngine.sh";

echo "\n";
echo "\n";
echo "\n";
echo "Use this token to start use the Jupyter notebook";


