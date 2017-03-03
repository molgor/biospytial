= Installation Notes

This document explains how to install the Biospytial full suite including the Postgres and Neo4J backends.

The system uses a customised version of Postgres/Postgis and Neo4J that are available in https://hub.docker.com/r/molgor: 

First initialize the Posgis container and Database as explained in the documentation. 

Or simply run:
    docker run \
    --name=postgis \
    --net=biospytial_network \
    -d \
    --publish=5432:5432 \
    --volume=/home/juan/DataVolumesBank/postgis:/DataVolumes \
    molgor/postgis_biospytial \
    /bin/sh -c "bash INITIALISATION_NOTES"

# Wait until the container finishes. 
See docker ps for inspecting availability.


Notes: This will only create the file structure.
It may be need to remove the container first to initialize it properly.

    docker rm postgis
    
    
    
## For starting the Container normally run:
    docker run \
    --name=postgis \
    --net=biospytial_network \
    -d \
    --publish=5432:5432 \
    --volume=/home/juan/DataVolumesBank/postgis:/DataVolumes \
    --volume=/mnt/data1:/mnt/data1 \
    molgor/postgis_biospytial \
    /bin/sh -c "/root/startPostgres"
        
 
## Load the neo4j container.
    docker run \
     --name=neo4j \
     --detach \
     --env NEO4J_AUTH=none \
     --publish=7474:7474 \
     --publish=7687:7687 \
     --volume=/home/juan/DataVolumesBank/neo4j/data:/data \
     --volume=/home/juan/DataVolumesBank/neo4j/logs:/logs \
     --net=biospytial_network \
     neo4j:3.1

 
 ## Once the two containers are running you may proceed with biospytial
 
    docker run \
     --name=biospytial \
     --publish=8000:8000 \
     --rm \
     --volume=/mnt/data1/RawDataCSV:/RawDataCSV \
     --volume=/home/juan/git-projects/biospytial:/apps \
     --volume=/mnt/data1:/mnt/data1 \
     --net=biospytial_network \
     -ti molgor/biospytial bash
 

## Set-up the suite.
There are some modules and functions that need to be installed before any prior usage.

1. Define the tables for occurrences
python manage.py migrate

2. INstall SQL functions and ability to manage GRIDS.

/SQL_functions/install_mesh_functions postgis biospytial

Note: Remeber that the password is biospytial.


## Inserting world borders
### From the biospytial console (not ipython) run
psql -d biospytial -U biospytial -h postgis -f TM_WORLD_BORDERS-0.3.sql

## Inserting the Raster Data.
### From the biospytial console (no ipython) locate the data directory (bioclim)
deactivate the biospytial environment with:
    source deactivate
    (to activate again run: source activate biospytial)
    
BETTER OPTION
INSIDE THE CONTAINER POSTGIS
### If the container is running just exec a console
docker exec -it postgis /bin/bash

Inside the container go to the data partition (/mnt/data1/bioclim/worldclim/) and run:
    for d in $(cat directories);
    do
		echo $d;
 		./migrateToPostgis.bash $d
	done









We need to have the data accesible. 
In this server it is located in:
/mnt/data1
If you can find it please contact me: molgor@gmail.com









        
  