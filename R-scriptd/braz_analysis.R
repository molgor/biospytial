library("sp","rgdal")
#ogrListLayers("/Users/juan/git_projects/biospatial/out_maps/taxs_8.shp")



#mesh64=readOGR("/Users/juan/git_projects/biospatial/out_maps/taxs_64.shp", layer="taxs_64") 
#will load the shapefile to your dataset.

m8=readOGR("/Users/juan/git_projects/biospatial/out_maps/taxs_8.shp", layer="taxs_8") 
m9=readOGR("/Users/juan/git_projects/biospatial/out_maps/taxs_9.shp", layer="taxs_9") 
m10=readOGR("/Users/juan/git_projects/biospatial/out_maps/taxs_10.shp", layer="taxs_10") 
m11=readOGR("/Users/juan/git_projects/biospatial/out_maps/taxs_11.shp", layer="taxs_11") 
m12=readOGR("/Users/juan/git_projects/biospatial/out_maps/taxs_12.shp", layer="taxs_12") 
m13=readOGR("/Users/juan/git_projects/biospatial/out_maps/taxs_13.shp", layer="taxs_13") 
m14=readOGR("/Users/juan/git_projects/biospatial/out_maps/taxs_14.shp", layer="taxs_14") 
m15=readOGR("/Users/juan/git_projects/biospatial/out_maps/taxs_15.shp", layer="taxs_15") 

#Without taking zero samples / disregarding places with no samples
m15.species.pres=subset(m15$species, m15$species > 0)
m14.species.pres=subset(m14$species, m14$species > 0)
m13.species.pres=subset(m13$species, m13$species > 0)
m12.species.pres=subset(m12$species, m12$species > 0)
m11.species.pres=subset(m11$species, m11$species > 0)
m10.species.pres=subset(m10$species, m10$species > 0)
m9.species.pres=subset(m9$species, m9$species > 0)
m8.species.pres=subset(m8$species, m8$species > 0)


#species_mean=(c(mean(m14$species),mean(m13$species),mean(m12$species),mean(m11$species),mean(m10$species),mean(m9$species),mean(m8$species)))
species_mean=(c(mean(m15.species.pres),mean(m14.species.pres),mean(m13.species.pres),mean(m12.species.pres),mean(m11.species.pres),mean(m10.species.pres),mean(m9.species.pres),mean(m8.species.pres)))

species_sd=(c(sd(m14$species),sd(m13$species),sd(m12$species),sd(m11$species),sd(m10$species),sd(m9$species),sd(m8$species)))


boxplot(m10$species,m10$genera,m10$families,m10$orders,m10$classes,m10$phyla)
species = c(m8$species,m9$species,m10$species)



