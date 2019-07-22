#!/bin/bash
## Script for installing the engine.
## It only changes some permissions and symbolic links to the .env file

## Change permission to make executables
chmod -c a+x startEngine.sh;

chmod -c a+x stopEngine.sh;

chmod -c a+x getJupyterToken.sh;

rm .env

ln -s container_files/.env .env

echo "Done! proceed to read HOW_TO_INSTALL.md"

