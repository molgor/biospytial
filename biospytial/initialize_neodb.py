# This script contains the constraints for the GRaph Database.
# While adding more data it would be necessary to put the corresponding constraints here

from py2neo import Graph
from biospytial import settings
neoparams = settings.NEO4J_DATABASES['default']
uri = "http://%(HOST)s:%(PORT)s%(ENDPOINT)s" % neoparams
g = Graph(uri)

# For Taxonomies
# g.schema.create_uniqueness_constraint("Root","id")
# g.schema.create_uniqueness_constraint("Kingdom","keyword")
# g.schema.create_uniqueness_constraint("Phylum","keyword")
# g.schema.create_uniqueness_constraint("Class","keyword")
# g.schema.create_uniqueness_constraint("Order","keyword")
# g.schema.create_uniqueness_constraint("Family","keyword")
# g.schema.create_uniqueness_constraint("Genus","keyword")
# g.schema.create_uniqueness_constraint("Specie","keyword")
# g.schema.create_uniqueness_constraint("Occurrence","pk")
# 
# g.schema.create_index("Kingdom","name")
#g.schema.create_index("Phylum","name")
#g.schema.create_index("Class","name")
#g.schema.create_index("Order","name")
#g.schema.create_index("Family","name")
#g.schema.create_index("Genus","name")
#g.schema.create_index("Specie","name")

#g.schema.create_uniqueness_constraint("Kingdom","id")
#g.schema.create_uniqueness_constraint("Phylum","id")
#g.schema.create_uniqueness_constraint("Class","id")
#g.schema.create_uniqueness_constraint("Order","id")
#g.schema.create_uniqueness_constraint("Family","id")
#g.schema.create_uniqueness_constraint("Genus","id")
#g.schema.create_uniqueness_constraint("Specie","id")


#g.schema.create_index("Kingdom","id")
#g.schema.create_index("Phylum","id")
#g.schema.create_index("Class","id")
#g.schema.create_index("Order","id")
#g.schema.create_index("Family","id")
#g.schema.create_index("Genus","id")
#g.schema.create_index("Specie","id")


# 
# ## Indexes for names
# 
# CREATE INDEX ON : Kingdom(name);
# CREATE INDEX ON : Phylum(name);
# CREATE INDEX ON : Class(name);
# CREATE INDEX ON : Order(name);
# CREATE INDEX ON :Family(name);
# CREATE INDEX ON : Genus(name);
# CREATE INDEX ON : Specie(name);
# 
# CREATE INDEX ON : Kingdom(id);
# CREATE INDEX ON : Phylum(id);
# CREATE INDEX ON : Class(id);
# CREATE INDEX ON : Order(id);
# CREATE INDEX ON :Family(id);
# CREATE INDEX ON : Genus(id);
# CREATE INDEX ON : Specie(id);
# CREATE INDEX ON : Occurrence(pk);

#### Indexes for Raster Data
#CREATE INDEX ON :`WindSpeed-30s`(uniqueid)
#CREATE INDEX ON :`Vapor-30s`(uniqueid)
#CREATE INDEX ON :`MinTemp-30s`(uniqueid)
#CREATE INDEX ON :`MeanTemp-30s`(uniqueid)
#CREATE INDEX ON :`SlrRad-30s`(uniqueid)
#CREATE INDEX ON :`Prec-30s`(uniqueid)
#CREATE INDEX ON :`MaxTemp-30s`(uniqueid)

