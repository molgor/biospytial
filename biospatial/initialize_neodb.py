# This script contains the constraints for the GRaph Database.
# While adding more data it would be necessary to put the corresponding constraints here

from py2neo import Graph

g = Graph()

# For Taxonomies
g.schema.create_uniqueness_constraint("Root","id")
g.schema.create_uniqueness_constraint("Kingdom","keyword")
g.schema.create_uniqueness_constraint("Phylum","keyword")
g.schema.create_uniqueness_constraint("Class","keyword")
g.schema.create_uniqueness_constraint("Order","keyword")
g.schema.create_uniqueness_constraint("Family","keyword")
g.schema.create_uniqueness_constraint("Genus","keyword")
g.schema.create_uniqueness_constraint("Specie","keyword")
g.schema.create_uniqueness_constraint("Occurrence","pk")

# For mesh
g.schema.create_uniqueness_constraint("Cell","uniqueid")


