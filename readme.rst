BiosPytial
==========
*An interactive / command-line modeller's suite for analyzing biodiversity across scales and space.*
Biospytial is a set of tools written in the Python programming language
that allows the identification of biodiversity patterns in space.
It uses the GBIF database, the biggest repository of species records in the world.

Datasource
----------



*"The Global Biodiversity Information Facility (GBIF) is an international open data infrastructure, funded by governments.
It allows anyone, anywhere to access data about all types of life on Earth, shared across national boundaries via the Internet.""*
`GBIF <http://gbif.org>``

Biospytial uses the GBIF dataset as principal input provider.
The data is then imported into a Postgis instance and managed by Django using REST and ORM interface.

There is a network representation that will work with Neo4j instead of the pickle-Redis implementation.



 Each occurrence has information about:

* Location (Lat/Long  EPSG:4326)
* Species
* Genus
* Family
* Order
* Class
* Phylum
* Kingdom
* Timestamp
* Country
* Collect - Id

See model gbif for more information.

Currently the entire GBIF database is mirrored

Bios`py`tial uses the Django framework to build complex object representation of
 biological occurrences.
