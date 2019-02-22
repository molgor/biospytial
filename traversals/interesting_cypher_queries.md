
#Get all the ocurrences for a given specie

Match (c:Specie)-[:IS_PARENT_OF]->(o:Occurrence)  RETURN c,o

# Get, filter by date
Match (c:Specie)-[:IS_PARENT_OF]->(o:Occurrence) WHERE o.year = 1939 RETURN c,o

# GEt a table type
Match (c:Specie)-[:IS_PARENT_OF]->(o:Occurrence)  RETURN c.name,o.name

#Get counts as a group by
Match (c:Specie)-[:IS_PARENT_OF]->(o:Occurrence)  RETURN c.name,count(o)

#SOrt by degree
Match (c:Specie)-[:IS_PARENT_OF]->(o:Occurrence)  RETURN c.name,count(o) as chocho ORDER BY chocho DESC


# Show all the tree
MATCH (r:Root)-[:IS_PARENT_OF*..7]->(s) return s

# Show complete taxonomy of a given occurrence
Let occurrence.pk = 875714 be an arbitrary id number 
MATCH (r: Occurrence {pk:875714})-[d :IS_A_MEMBER_OF*..8]->(s) return d

#  FLowering families of plants that can be polinated by bees within the neighbours that have records of the family Apidae

MATCH (abeja:Family {name:'Apidae'})-[r1: IS_IN]->(c:Cell)-[IS_NEIGHBOUR_OF]->(n:Cell)
<-[r2: IS_IN]-(plant: Kingdom {name:'Plantae'})-[IS_PARENT_OF]->
(d :Phylum {name: 'Magnoliophyta'} )-[r4 : IS_PARENT_OF*..3]->
(f: Family) 
WITH f RETURN DISTINCT f.name

# Canidae and the families of vertebrates
MATCH (carnisaurio:Family {name:'Canidae'})-[r1: IS_IN]->(c:Cell)-[IS_NEIGHBOUR_OF]->(n:Cell)
<-[r2: IS_IN]-(plant: Kingdom {name:'Animalia'})-[IS_PARENT_OF]->
(d :Phylum {name: 'Chordata'} )-[r4 : IS_PARENT_OF*..2]->
(f: Order) 
WITH f RETURN DISTINCT f.name

## Some examples
MATCH (carnisaurio:Family {name:'Canidae'})-[r1: IS_IN]->(c:Cell)-[IS_NEIGHBOUR_OF]->(n:Cell)
<-[r2: IS_IN]-(animals: Kingdom {name:'Animalia'})-[IS_PARENT_OF]->
(d :Phylum {name: 'Chordata'} )-[r4 : IS_PARENT_OF*..3]->
(f)-[HAS_EVENT]->(o : Occurrence)-[Elevation]->(e) 
WHERE f.name <> 'Canidae' 
Return o
ORDER BY o.event_date
LIMIT 100



## Erase taxonomic nodes
MATCH (o:Root) DETACH DELETE o ;
MATCH (o:Kingdom) DETACH DELETE o;
MATCH (o:Phylum) DETACH DELETE o;
MATCH (o:Class) DETACH DELETE o;
MATCH (o:Order) DETACH DELETE o;
MATCH (o:Family) DETACH DELETE o;
MATCH (o:Genus) DETACH DELETE o;
MATCH (o:Species) DETACH DELETE o;
MATCH (o:Occurrence) DETACH DELETE o;

MATCH (o:`WindSpeed-30s`) DETACH DELETE o;
MATCH (o:`Vapor-30s`) DETACH DELETE o;
MATCH (o:`SirRad-30s`) DETACH DELETE o;
MATCH (o:`Prec-30s`) DETACH DELETE o;
MATCH (o:`MaxTemp-30s`) DETACH DELETE o;
MATCH (o:`MeanTemp-30s`) DETACH DELETE o;
MATCH (o:`MinTemp-30s`) DETACH DELETE o;
MATCH (o:DEM_12) DETACH DELETE o;


# Distances
## To get the shortest path route between two nodes
MATCH path=shortestPath((n:Genus{name: 'Ursus'})-[:IS_PARENT_OF*]-(p:Genus{name: 'Romerolagus'})) Return path

This uses the relation 'IS_PARENT_OF'. To use any other relation 'r' do:

MATCH path=shortestPath((n:Genus{name: 'Ursus'})-[:r*]-(p:Genus{name: 'Romerolagus'})) Return path


MATCH path1=(oso: Genus{name: 'Ursus'})-[: IS_A_MEMBER_OF*]->(root)

MATCH path2 = (cone: Genus{name: 'Romerolagus'}) -[: IS_A_MEMBER_OF*]->(root)

MATCH path1=((oso: Genus{name: 'Ursus'})-[: IS_A_MEMBER_OF*]->(osos))

MATCH path2=(cone: Genus{name: 'Romerolagus'}) -[: IS_A_MEMBER_OF*]->(cones)

UNWIND nodes(path1) as np1

RETURN collect(NOT(np1 IN nodes(path2)))

