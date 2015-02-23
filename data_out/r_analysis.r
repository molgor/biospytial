d = read.csv("/Users/juan/git_projects/biospatial/data_out/dets16_f.out")

svd = read.csv("/Users/juan/git_projects/biospatial/data_out/dets_16_svd.out")

red_d = read.csv("/Users/juan/git_projects/biospatial/data_out/red_dim_svd.out")

#Data preparation .
# Omit 'NA'
d_ = na.omit(d)
#standarize varibles
ds = scale(d_)

fit_d=kmeans(d_,10)

# vary parameters for most readable graph
library(cluster) 
clusplot(d_, fit_d$cluster, color=TRUE, shade=TRUE, 
         labels=2, lines=0)

# Centroid Plot against 1st 2 discriminant functions
library(fpc)
plotcluster(d_, fit_d$cluster)

################################
# FOR svd data


svd_ = na.omit(svd)
#standarize varibles
svds = scale(svd_)

fit_svd=kmeans(svd_,10)

fit_svd_scaled = kmeans(svds,10)

# vary parameters for most readable graph
library(cluster) 
clusplot(svd_, fit_svd$cluster, color=TRUE, shade=TRUE, 
         labels=2, lines=0)

# Centroid Plot against 1st 2 discriminant functions
library(fpc)
plotcluster(svd_, fit_svd$cluster)



### For red_d data
# FOR svd data


red_d_ = na.omit(red_d)
#standarize varibles
red_ds = scale(red_d_)

fit_red=kmeans(red_d_,10)

fit_red_scaled = kmeans(red_ds,10)

# vary parameters for most readable graph
library(cluster) 
clusplot(red_ds, fit_red_scaled$cluster, color=TRUE, shade=TRUE, 
         labels=2, lines=0)

# Centroid Plot against 1st 2 discriminant functions
library(fpc)
plotcluster(red_ds, fit_red_scaled$cluster)

ns = data.frame( red_d$gid,red_d$species,red_d$genera,red_d$families,red_d$orders,red_d$classes,red_d$phyla,red_d$kingdoms,fit_red_scaled$cluster )
write.csv(ns,'/Users/juan/git_projects/biospatial/data_out/kmeans_red_dim_16.csv')
