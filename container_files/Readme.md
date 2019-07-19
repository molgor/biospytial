# Container files for initialising *Biospytial* services
This folder contains the files needed for running a complete 
Biospytial suite. 

## File descriptions
* biospytial_stack.yml : the compose file for initialising the services in a linux host.
* biospytial_stackOSX.yml : the compose file to be run for Mac (OSX) host.

* standalone_file : The folder with compose file to be run the modules independently.

## How to configure the containers
The mounting points need to be change to a valid path in your system.
Each service (biospytial, neo4j, postgis and redis) has its own path.

## Biospytial Computing Engine
Where this code located.
Change the general `path` (e.g. /mnt/data1/) to a valid one according to your system. 
*`/mnt/data1/RawDataCSV`:   Where the raw CSV files are located. Useful to store files to be imported into the system.
*`/mnt/data1/outputs/`: The default path for storing output files.
*`/mnt/data1/git-projects/biospytial` : the path where Biospytial source code is located.


## Relational Geoprocessing Unit (Postgis)
Two mounting points are defined here:

* `/home/juan/DataVolumesBank/postgis` : where the database is located. It is recommended to be located in a fast drive (e.g. SSD).
* `/mnt/data1` : Shared partition common with *Biospytial*. Allows easy exchange of files.

## Graph Storage and Processing Unit (Neo4J)
Similarly to the postgis service, this service has a mounting point for storing the database and another for storing logs (administration purposes).
* `/opt/DataVolumesFast/neo4j/data` : where the graph database (neo4j) stores the data.
* `/opt/DataVolumesFast/neo4j/logs` : where the logs from the neo4j instance are stored.

## Message Broker System (Redis)
* `/home/juan/DataVolumesBank/redis` : where the redis data is stored. If used, it will store the key-valued database here. 


