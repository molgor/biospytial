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
species_mean=(c(mean(m15.species.pres),mean(m14.species.pres),mean(m13.species.pres),mean(m12.species.pres),mean(m11.species.pres),mean(m10.species.pres),mean(m9.species.pres),mean(m8.species.pres)))
species_sd=(c(sd(m14.species.pres),sd(m13.species.pres),sd(m12.species.pres),sd(m11.species.pres),sd(m10.species.pres),sd(m9.species.pres),sd(m8.species.pres)))

#Without taking zero samples / disregarding places with no samples
m15.genera=subset(m15$genera, m15$genera > 0)
m14.genera=subset(m14$genera, m14$genera > 0)
m13.genera=subset(m13$genera, m13$genera > 0)
m12.genera=subset(m12$genera, m12$genera > 0)
m11.genera=subset(m11$genera, m11$genera > 0)
m10.genera=subset(m10$genera, m10$genera > 0)
m9.genera=subset(m9$genera, m9$genera > 0)
m8.genera=subset(m8$genera, m8$genera > 0)
genera_mean=(c(mean(m15.genera),mean(m14.genera),mean(m13.genera),mean(m12.genera),mean(m11.genera),mean(m10.genera),mean(m9.genera),mean(m8.genera)))
genera_sd=(c(sd(m14.genera),sd(m13.genera),sd(m12.genera),sd(m11.genera),sd(m10.genera),sd(m9.genera),sd(m8.genera)))


m15.families=subset(m15$families, m15$families > 0)
m14.families=subset(m14$families, m14$families > 0)
m13.families=subset(m13$families, m13$families > 0)
m12.families=subset(m12$families, m12$families > 0)
m11.families=subset(m11$families, m11$families > 0)
m10.families=subset(m10$families, m10$families > 0)
m9.families=subset(m9$families, m9$families > 0)
m8.families=subset(m8$families, m8$families > 0)
families_mean=(c(mean(m15.families),mean(m14.families),mean(m13.families),mean(m12.families),mean(m11.families),mean(m10.families),mean(m9.families),mean(m8.families)))
families_sd=(c(sd(m14.families),sd(m13.families),sd(m12.families),sd(m11.families),sd(m10.families),sd(m9.families),sd(m8.families)))


m15.orders=subset(m15$orders, m15$orders > 0)
m14.orders=subset(m14$orders, m14$orders > 0)
m13.orders=subset(m13$orders, m13$orders > 0)
m12.orders=subset(m12$orders, m12$orders > 0)
m11.orders=subset(m11$orders, m11$orders > 0)
m10.orders=subset(m10$orders, m10$orders > 0)
m9.orders=subset(m9$orders, m9$orders > 0)
m8.orders=subset(m8$orders, m8$orders > 0)
orders_mean=(c(mean(m15.orders),mean(m14.orders),mean(m13.orders),mean(m12.orders),mean(m11.orders),mean(m10.orders),mean(m9.orders),mean(m8.orders)))
orders_sd=(c(sd(m14.orders),sd(m13.orders),sd(m12.orders),sd(m11.orders),sd(m10.orders),sd(m9.orders),sd(m8.orders)))


m15.classes=subset(m15$classes, m15$classes > 0)
m14.classes=subset(m14$classes, m14$classes > 0)
m13.classes=subset(m13$classes, m13$classes > 0)
m12.classes=subset(m12$classes, m12$classes > 0)
m11.classes=subset(m11$classes, m11$classes > 0)
m10.classes=subset(m10$classes, m10$classes > 0)
m9.classes=subset(m9$classes, m9$classes > 0)
m8.classes=subset(m8$classes, m8$classes > 0)
classes_mean=(c(mean(m15.classes),mean(m14.classes),mean(m13.classes),mean(m12.classes),mean(m11.classes),mean(m10.classes),mean(m9.classes),mean(m8.classes)))
classes_sd=(c(sd(m14.classes),sd(m13.classes),sd(m12.classes),sd(m11.classes),sd(m10.classes),sd(m9.classes),sd(m8.classes)))

m15.phyla=subset(m15$phyla, m15$phyla > 0)
m14.phyla=subset(m14$phyla, m14$phyla > 0)
m13.phyla=subset(m13$phyla, m13$phyla > 0)
m12.phyla=subset(m12$phyla, m12$phyla > 0)
m11.phyla=subset(m11$phyla, m11$phyla > 0)
m10.phyla=subset(m10$phyla, m10$phyla > 0)
m9.phyla=subset(m9$phyla, m9$phyla > 0)
m8.phyla=subset(m8$phyla, m8$phyla > 0)
phyla_mean=(c(mean(m15.phyla),mean(m14.phyla),mean(m13.phyla),mean(m12.phyla),mean(m11.phyla),mean(m10.phyla),mean(m9.phyla),mean(m8.phyla)))
phyla_sd=(c(sd(m14.phyla),sd(m13.phyla),sd(m12.phyla),sd(m11.phyla),sd(m10.phyla),sd(m9.phyla),sd(m8.phyla)))


m15.kingdoms=subset(m15$kingdoms, m15$kingdoms > 0)
m14.kingdoms=subset(m14$kingdoms, m14$kingdoms > 0)
m13.kingdoms=subset(m13$kingdoms, m13$kingdoms > 0)
m12.kingdoms=subset(m12$kingdoms, m12$kingdoms > 0)
m11.kingdoms=subset(m11$kingdoms, m11$kingdoms > 0)
m10.kingdoms=subset(m10$kingdoms, m10$kingdoms > 0)
m9.kingdoms=subset(m9$kingdoms, m9$kingdoms > 0)
m8.kingdoms=subset(m8$kingdoms, m8$kingdoms > 0)
kingdoms_mean=(c(mean(m15.kingdoms),mean(m14.kingdoms),mean(m13.kingdoms),mean(m12.kingdoms),mean(m11.kingdoms),mean(m10.kingdoms),mean(m9.kingdoms),mean(m8.kingdoms)))
kingdoms_sd=(c(sd(m14.kingdoms),sd(m13.kingdoms),sd(m12.kingdoms),sd(m11.kingdoms),sd(m10.kingdoms),sd(m9.kingdoms),sd(m8.kingdoms)))




#species_mean=(c(mean(m14$species),mean(m13$species),mean(m12$species),mean(m11$species),mean(m10$species),mean(m9$species),mean(m8$species)))


boxplot(m10$species,m10$genera,m10$families,m10$orders,m10$classes,m10$phyla)
species = c(m8$species,m9$species,m10$species)



plot(species_mean[1:5])

#par(pch
=22, col="red") # plotting symbol and color 
par(mfrow=c(2,2)) # all plots on one page 
plot(species_mean, type="l", main='species richness',xlab='Scale level',ylab='mean richness') 
plot(genera_mean, type="l", main='genera richness',xlab='Scale level',ylab='mean richness')
plot(families_mean, type="l", main='families richness',xlab='Scale level',ylab='mean richness') 
plot(orders_mean, type="l", main='orders richness',xlab='Scale level',ylab='mean richness')
plot(classes_mean, type="l", main='classes richness',xlab='Scale level',ylab='mean richness') 
plot(phyla_mean, type="l", main='phyla richness',xlab='Scale level',ylab='mean richness') 
plot(kingdoms_mean, type="l", main='kingdoms richness',xlab='Scale level',ylab='mean richness') 

taxscales = ()
extractSpecie = function(taxonomicLayer) {
  
}

species = data.frame(m8$species,m9$species,m10$species,m11$species,m12$species,m13$species,m14$species,m15$species)
buscar spatial variance analysis
