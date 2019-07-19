# Drivers for data models
This folder contains the specifications and tools for data models stored in the Graph database. 
This includes:
## Graph drivers for Neo4J
This includes simple class definitions for:
* Cells
* Grids
* Raster Nodes (converting raster pixel values to node) 

It also includes specifications for complex graph traversals like:
* TreeNode
* TreeNeo
* and different taxonomic levels

### Files to be consider are:
* `graph_models.py`
* `tree_builder.py`
* `encoders.py`


## Tools for taxonomic trees (TreeNeo) objects
These tools are located in:
`tools.py` and includes:
* Interactive visualisation
* Node ranking by frequency
* Connection to Messaging Broker
* Convert trees to Tables


## Tools for ingestion of GBIF data
This ingestion assumes that the raw data is distributed in a CSV file format or directly from the GBIF API. 
Files to be consider are:
* `csv_raw_loader.py`
* `populate.csv`


## Admin tools for manual data ingestion using django API
* `admin.py`

