# This is a script for loading all the necessary data for processing 
# i.e. it is a preprocessing script.
# Change it appropriately

#file = '/outputs/presence_only_models/predictors/dataset100x100-puebla-p9/0-pred.csv'
#PDF = read.csv(file)
## REad adjancency matrix

## Load Stuff
library(CARBayes)
library(dplyr)
library(purrr)
library(reticulate)
library(biospytial.rwrapper)

# Import adjancency matrix generated from region
mat_filename = "/outputs/training_data_sample_puebla_p9_abies_pinophyta_adjmat.npy"
# Use numpy functions
np <- import("numpy")
M <- np$load(mat_filename)

## Training data.frame
TDF = read.csv("/outputs/training_data_sample_puebla_p9_abies_pinophyta.csv")

## Order it according to the id of the cell
### This is important because the adjancy matrix rows need to be the same
TDF = TDF[order(TDF$cell_ids),]
# Convert to numeric
TDF = mutate_at(TDF,vars(Dist.to.road_m,Elevation_m,
                         MaxTemp_m,MeanTemp_m,
                         MinTemp_m,Population_m,
                         Precipitation_m,
                         SolarRadiation_m,
                         VaporPres_m,
                         WindSp_m),as.numeric)
# Remove unnecessary symbols in variable names
names(TDF) = lapply(names(TDF),function(x) gsub("_","",x))
names(TDF) = lapply(names(TDF),function(x) gsub("\\.","",x))
                    
## Remove entries with zero neighbours (adjancey matrix)
### Calculates number of neighbours in D (sum)
D = apply(M,MARGIN = 1,sum)
### get index with 0 neighbours
idx = match(0,D)
### select cells with no neighbours
cell_with_no_neighbour = TDF$cellids[idx]

## Erase idx for M and for TDF (Or maybe only for M)
M_bis = M[-c(idx),-c(idx)]

###
# Preprocess for generating pseudo absences
# Change the name of a column that for some reason is called the same
names(TDF)[23] <- 'covid2'
DataFrame = TDF %>% rowwise() %>% 
            mutate(sample=pseudo_absence_naive(Plantae,LUCA),species=pseudo_absence_naive(Pinophyta,Plantae))

###
# Formula definition
formula_sample=sample~Disttoroadm+Populationm #+factor(tipos)
formula_presence=species~Elevationm+MeanTempm
n <- nrow(TDF)
trials <- rep(1,n)






