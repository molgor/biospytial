![Biospytial logo](biospytial.png)

Biospytial is a modular open source knowledge engine designed to import, organise, analyse and visualise big spatial ecological datasets using the power of graph theory. 
It handles species occurrences and their taxonomic classification for performing ecological analysis on biodiversity and species distributions.

The engine uses a hybrid graph-relational approach to store and access information linked with relationships that are stored in a graph database, while tabular and geospatial (vector and raster) data are stored in a relational database management system (Postgis 9.x). 
The graph data structure provides a scalable design that eases the problem of merging datasets from different sources.

The linkage relationships use semantic structures (objects and predicates) to answer scientific questions represented as complex data structures stored in the graph database.

Biospytial comprises three interconnected components:

1. Geospatial Processing unit (GPU) supported by a RDBMS with geoprocessing capabilities
2. Graph Storage and Querying Unit (supported by Neo4J)
3. A graph-relational package, The Biospytial Computing Engine (BCE) that integrates all the system’s components. 

>> It also includes tools like: interactive notebooks and command-line suite for analyzing biodiversity across scales and space.*

## Installation
The suite is currently installed in a Docker container. (molgor/biospytial)
It uses a neo4j and a postgis backend that can be found in the molgor repository in the Docker Hub.
Instructions for installing are located [here](HOW_TO_INSTALL.md)

## Running Biospytial in Jupyter mode:
The jupyter notebook is automatically loaded. To access it use a webbrowser and go to the following url:

  * [http://localhost:8888](http://localhost:8888)

If a token is requested run the following command:

```
./getJupyterToken.sh
```
Copy the 
Use the token value and paste it in the webpage.

### Example notebooks
Currently there are two examples, more are coming!

* [Jaguar example](http://localhost:8888/notebooks/examples/%5BOfficial%20Demo%5DCo-ocurrences_Jaguar.ipynb)
* [Raster example](http://localhost:8888/notebooks/examples/Basic%20Raster%20Tools%20in%20Biospytial.ipynb)


## Login using command-line console
Use the ssh service

```
ssh -p 2323 biospytial@localhost 
```
The password is `biospytial.`

>> It is recommended to change this password if it is intended to use in operational mode.

Happy coding :smile:


# Demonstration:
[Video](https://www.youtube.com/watch?v=C96ZiHAODSE)



## Visualising the processes
We can load a process visualizer to see if everything is working properly

```
docker run -it -d -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock dockersamples/visualizer
```
Visit the webpage [your_host]:8080

# Data for using the Biospytial Engine

## Dataset needed for running the system
The datasets are available in  binary format to be run by the *Biospytial* system.
This include the necessary data for running the examples provided in the manuscript 
submitted to a peer-reviewed journal. 


## Content of the data package
There are two folders here:
* `postgisdb` : the binary data files used by the Relational Geoprocessing Unit (RGP) 
* `neo4jdb` : the binary data files used by the Graph Storage and Processing Unit (GSPU)

## Mounting the data into the system 
The two folders should be mounted on their respective module (service in docker jargon).
This is done by adding the absolute path of these folders into the docker compose file.

* The name of the service for the RGP is *postgis*. 
* The name of the service for the GSPU is *neo4j*.

The PATH to change is in the section: `volumes`

### For example:
Assuming that the path for the data is:
`/home/foo/biospytial-data`
The `volume` section should be changed to:

```
  volumes:
   - '/home/foo/biospytial-data/postgisdb:/DataVolumes'
```

Similarly for the neo4j service:

```
  volumes:
   - '/home/foo/biospytial-data/neo4jdb:/DataVolumes'
```

### Location
The docker compose files are stored in the *Biospytial* source code, inside the folder `container_files`. 
These files are:

* `biospytial_stack.yml` (Linux) 
* `biospytial_stackOSX.yml` (Mac) 

### Data availability
The software is under review, data will be available after passing this stage.


Date: July 23th, 2019
Author: Juan Escamilla Molgora



