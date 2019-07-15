# This is a script for loading all the necessary data for processing 
# i.e. it is a preprocessing script.
# Change it appropriately

#my.binomial.bymCAR <- function(formula, data=NULL, trials, W, burnin, n.sample, thin=1, prior.mean.beta=NULL, prior.var.beta=NULL, prior.tau2=NULL, prior.sigma2=NULL, MALA=TRUE, verbose=TRUE)


#my.binomial.bymCAR(formula=formula_sample,W=M_bis,trials = trials,data=TDF,burnin=10000,n.sample=15000,verbose = TRUE)


#model.sample <-S.CARbym(formula=formula_sample,family="binomial",W=M_bis,trials = trials,data=TDF,burnin=10000,n.sample=15000,verbose = TRUE)

### Order of the code to be executed
# 1. Load init_data
# 2. Load imports.R
# 3. Load as function my_CARbym in S.CARbym.R
# 4. Load as function my.binomial.bymCAR in my.binomial.bymCAR.R
# 5. Run the above line

model.sample <-my_CARbym(formula=formula_sample,family="binomial",W=M_bis,trials = trials,data=TDF,burnin=10000,n.sample=15000,verbose = TRUE,custom_function=my.binomial.bymCAR) 


#### Init data sandboxing the carsampler

#n.sample = 2
#n.miss <- frame.results$n.miss 

## Preload the stuff
source("init_data.R")
# imports
source("imports.R")
# load the building function
source("samplerCarFunction.R")




formula_sample = sample ~ Disttoroadm + Populationm
frame.results <- common.frame(formula_sample, DataFrame, "binomial")


which.miss <- frame.results$which.miss

sampler(n.sample=2,n.miss=frame.results$n.miss,
       which.miss = frame.results$which.miss
        )

## clean workspace
rm(list=ls())









