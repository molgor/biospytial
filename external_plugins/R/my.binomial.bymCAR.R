my.binomial.bymCAR <- function(formula, data=NULL, trials, W, burnin, n.sample, thin=1, prior.mean.beta=NULL, prior.var.beta=NULL, prior.tau2=NULL, prior.sigma2=NULL, MALA=TRUE, verbose=TRUE)
{
##############################################
#### Format the arguments and check for errors
##############################################
#### Verbose
a <- common.verbose(verbose)
    
    
#### Frame object
frame.results <- common.frame(formula, data, "binomial")
K <- frame.results$n
p <- frame.results$p
X <- frame.results$X
X.standardised <- frame.results$X.standardised
X.sd <- frame.results$X.sd
X.mean <- frame.results$X.mean
X.indicator <- frame.results$X.indicator 
offset <- frame.results$offset
Y <- frame.results$Y
which.miss <- frame.results$which.miss
n.miss <- frame.results$n.miss  
Y.DA <- Y

    
#### Check on MALA argument
    if(length(MALA)!=1) stop("MALA is not length 1.", call.=FALSE)
    if(!is.logical(MALA)) stop("MALA is not logical.", call.=FALSE)  


#### Check and format the trials argument
    if(sum(is.na(trials))>0) stop("the numbers of trials has missing 'NA' values.", call.=FALSE)
    if(!is.numeric(trials)) stop("the numbers of trials has non-numeric values.", call.=FALSE)
int.check <- K-sum(ceiling(trials)==floor(trials))
    if(int.check > 0) stop("the numbers of trials has non-integer values.", call.=FALSE)
    if(min(trials)<=0) stop("the numbers of trials has zero or negative values.", call.=FALSE)
failures <- trials - Y
failures.DA <- trials - Y.DA
    if(sum(Y>trials, na.rm=TRUE)>0) stop("the response variable has larger values that the numbers of trials.", call.=FALSE)


#### Priors
    if(is.null(prior.mean.beta)) prior.mean.beta <- rep(0, p)
    if(is.null(prior.var.beta)) prior.var.beta <- rep(100000, p)
    if(is.null(prior.tau2)) prior.tau2 <- c(1, 0.01)
    if(is.null(prior.sigma2)) prior.sigma2 <- c(1, 0.01)
common.prior.beta.check(prior.mean.beta, prior.var.beta, p)
common.prior.var.check(prior.tau2)
common.prior.var.check(prior.sigma2)


## Compute the blocking structure for beta     
block.temp <- common.betablock(p)
beta.beg  <- block.temp[[1]]
beta.fin <- block.temp[[2]]
n.beta.block <- block.temp[[3]]
list.block <- as.list(rep(NA, n.beta.block*2))
    for(r in 1:n.beta.block)
    {
    list.block[[r]] <- beta.beg[r]:beta.fin[r]-1
    list.block[[r+n.beta.block]] <- length(list.block[[r]])
    }


#### MCMC quantities - burnin, n.sample, thin
common.burnin.nsample.thin.check(burnin, n.sample, thin)



#############################
#### Initial parameter values
#############################
dat <- cbind(Y, failures)
mod.glm <- glm(dat~X.standardised-1, offset=offset, family="quasibinomial")
beta.mean <- mod.glm$coefficients
beta.sd <- sqrt(diag(summary(mod.glm)$cov.scaled))
beta <- rnorm(n=length(beta.mean), mean=beta.mean, sd=beta.sd)

theta.hat <- Y / trials
theta.hat[theta.hat==0] <- 0.01
theta.hat[theta.hat==1] <- 0.99
res.temp <- log(theta.hat / (1 - theta.hat)) - X.standardised %*% beta.mean - offset
res.sd <- sd(res.temp, na.rm=TRUE)/5
phi <- rnorm(n=K, mean=rep(0,K), sd=res.sd)
tau2 <- var(phi) / 10
theta <- rnorm(n=K, mean=rep(0,K), sd=res.sd)
sigma2 <- var(theta) / 10
lp <- as.numeric(X.standardised %*% beta) + phi + theta + offset
prob <- exp(lp)  / (1 + exp(lp))


###############################    
#### Set up the MCMC quantities    
###############################
#### Matrices to store samples
n.keep <- floor((n.sample - burnin)/thin)
samples.beta <- array(NA, c(n.keep, p))
samples.re <- array(NA, c(n.keep, K))
samples.tau2 <- array(NA, c(n.keep, 1))
samples.sigma2 <- array(NA, c(n.keep, 1))
samples.loglike <- array(NA, c(n.keep, K))
samples.fitted <- array(NA, c(n.keep, K))
if(n.miss>0) samples.Y <- array(NA, c(n.keep, n.miss))

  
#### Metropolis quantities
accept.all <- rep(0,6)
accept <- accept.all
proposal.sd.beta <- 0.01
proposal.sd.phi <- 0.1
proposal.sd.theta <- 0.1
tau2.posterior.shape <- prior.tau2[1] + 0.5 * (K-1)
sigma2.posterior.shape <- prior.sigma2[1] + 0.5 * K 
 


##################################
#### Set up the spatial quantities
##################################
#### CAR quantities
W.quants <- common.Wcheckformat(W)
W <- W.quants$W
W.triplet <- W.quants$W.triplet
n.triplet <- W.quants$n.triplet
W.triplet.sum <- W.quants$W.triplet.sum
n.neighbours <- W.quants$n.neighbours 
W.begfin <- W.quants$W.begfin


#### Check for islands
W.list<- mat2listw(W)
W.nb <- W.list$neighbours
W.islands <- n.comp.nb(W.nb)
islands <- W.islands$comp.id
n.islands <- max(W.islands$nc)
tau2.posterior.shape <- prior.tau2[1] + 0.5 * (K-n.islands)   



###########################
#### Run the Bayesian model
###########################
#### Start timer
    if(verbose)
    {
    cat("Generating mamamai function!", n.keep, "post burnin and thinned (if requested) samples.\n", sep = " ")
    progressBar <- txtProgressBar(style = 3)
    percentage.points<-round((1:100/100)*n.sample)
    }else
    {
    percentage.points<-round((1:100/100)*n.sample)     
    }


#### Create the MCMC samples      
    for(j in 1:n.sample)
    {
    ####################################
    ## Sample from Y - data augmentation
    ####################################
        if(n.miss>0)
        {
        Y.DA[which.miss==0] <- rbinom(n=n.miss, size=trials[which.miss==0], prob=prob[which.miss==0])
        failures.DA <- trials - Y.DA
        }else
        {}
        
        
        
    ####################
    ## Sample from beta
    ####################
    offset.temp <- phi + offset + theta
        if(p>2)
        {
        temp <- binomialbetaupdateMALA(X.standardised, K, p, beta, offset.temp, Y.DA, failures.DA, trials, prior.mean.beta, prior.var.beta, n.beta.block, proposal.sd.beta, list.block)
        }else
        {
        temp <- binomialbetaupdateRW(X.standardised, K, p, beta, offset.temp, Y.DA, failures.DA, prior.mean.beta, prior.var.beta, proposal.sd.beta)
        }
    beta <- temp[[1]]
    accept[1] <- accept[1] + temp[[2]]
    accept[2] <- accept[2] + n.beta.block  



    ####################
    ## Sample from phi
    ####################
    beta.offset <- X.standardised %*% beta + theta + offset
        if(MALA)
        {
        temp1 <- binomialcarupdateMALA(Wtriplet=W.triplet, Wbegfin=W.begfin, Wtripletsum=W.triplet.sum, nsites=K, phi=phi, tau2=tau2, y=Y.DA, failures=failures.DA, trials=trials, phi_tune=proposal.sd.phi, rho=1, offset=beta.offset)
        }else
        {
        temp1 <- binomialcarupdateRW(Wtriplet=W.triplet, Wbegfin=W.begfin, Wtripletsum=W.triplet.sum, nsites=K, phi=phi, tau2=tau2, y=Y.DA, failures=failures.DA, phi_tune=proposal.sd.phi, rho=1, offset=beta.offset)
        }
    phi <- temp1[[1]]
    phi[which(islands==1)] <- phi[which(islands==1)] - mean(phi[which(islands==1)])
    accept[3] <- accept[3] + temp1[[2]]
    accept[4] <- accept[4] + K
     
    

    ####################
    ## Sample from theta
    ####################
    beta.offset <- as.numeric(X.standardised %*% beta) + phi + offset
        if(MALA)
        {
        temp2 <- binomialindepupdateMALA(nsites=K, theta=theta, sigma2=sigma2, y=Y.DA, failures=failures.DA, trials=trials, theta_tune=proposal.sd.theta, offset=beta.offset) 
        }else
        {
        temp2 <- binomialindepupdateRW(nsites=K, theta=theta, sigma2=sigma2, y=Y.DA, failures=failures.DA, theta_tune=proposal.sd.theta, offset=beta.offset) 
        }
    theta <- temp2[[1]]
    theta <- theta - mean(theta)    
    accept[5] <- accept[5] + temp2[[2]]
    accept[6] <- accept[6] + K          
     


    ###################
    ## Sample from tau2
    ###################
    temp2 <- quadform(W.triplet, W.triplet.sum, n.triplet, K, phi, phi, 1)    
    tau2.posterior.scale <- temp2 + prior.tau2[2] 
    tau2 <- 1 / rgamma(1, tau2.posterior.shape, scale=(1/tau2.posterior.scale))
    
    
    
    #####################
    ## Sample from sigma2
    #####################
    sigma2.posterior.scale <- prior.sigma2[2] + 0.5*sum(theta^2)
    sigma2 <- 1 / rgamma(1, sigma2.posterior.shape, scale=(1/sigma2.posterior.scale))
    
    
    
    #########################
    ## Calculate the deviance
    #########################
    lp <- as.numeric(X.standardised %*% beta) + phi + theta + offset
    prob <- exp(lp)  / (1 + exp(lp))
    fitted <- trials * prob
    loglike <- dbinom(x=Y, size=trials, prob=prob, log=TRUE)


    
    ###################
    ## Save the results
    ###################
        if(j > burnin & (j-burnin)%%thin==0)
        {
        ele <- (j - burnin) / thin
        samples.beta[ele, ] <- beta
        samples.re[ele, ] <- phi + theta
        samples.tau2[ele, ] <- tau2
        samples.sigma2[ele, ] <- sigma2
        samples.loglike[ele, ] <- loglike
        samples.fitted[ele, ] <- fitted
            if(n.miss>0) samples.Y[ele, ] <- Y.DA[which.miss==0]
        }else
        {
        }


    
    ########################################
    ## Self tune the acceptance probabilties
    ########################################
    k <- j/100
        if(ceiling(k)==floor(k))
        {
        #### Update the proposal sds
            if(p>2)
            {
            proposal.sd.beta <- common.accceptrates1(accept[1:2], proposal.sd.beta, 40, 50)
            }else
            {
            proposal.sd.beta <- common.accceptrates1(accept[1:2], proposal.sd.beta, 30, 40)    
            }
        proposal.sd.phi <- common.accceptrates1(accept[3:4], proposal.sd.phi, 40, 50)
        proposal.sd.theta <- common.accceptrates1(accept[5:6], proposal.sd.theta, 40, 50)
        accept.all <- accept.all + accept
        accept <- c(0,0,0,0,0,0)
        }else
        {   
        }
    
    
    
    ################################       
    ## print progress to the console
    ################################
          if(j %in% percentage.points & verbose)
          {
          setTxtProgressBar(progressBar, j/n.sample)
          }
     }

##### end timer
    if(verbose)
    {
    cat("\nSummarising results.")
    close(progressBar)
    }else
    {}



###################################
#### Summarise and save the results 
###################################
#### Compute the acceptance rates
accept.beta <- 100 * accept.all[1] / accept.all[2]
accept.phi <- 100 * accept.all[3] / accept.all[4]
accept.theta <- 100 * accept.all[5] / accept.all[6]
accept.tau2 <- 100
accept.sigma2 <- 100
accept.final <- c(accept.beta, accept.phi, accept.theta, accept.tau2, accept.sigma2)
names(accept.final) <- c("beta", "phi", "theta", "tau2", "sigma2")

     
#### Compute the fitted deviance
mean.beta <- apply(samples.beta, 2, mean)
mean.re <- apply(samples.re, 2, mean)
mean.logit <- as.numeric(X.standardised %*% mean.beta) + mean.re + offset    
mean.prob <- exp(mean.logit)  / (1 + exp(mean.logit))
fitted.mean <- trials * mean.prob
deviance.fitted <- -2 * sum(dbinom(x=Y, size=trials, prob=mean.prob, log=TRUE), na.rm=TRUE)


#### Model fit criteria
modelfit <- common.modelfit(samples.loglike, deviance.fitted)


#### transform the parameters back to the origianl covariate scale.
samples.beta.orig <- common.betatransform(samples.beta, X.indicator, X.mean, X.sd, p, FALSE)


#### Create a summary object
samples.beta.orig <- mcmc(samples.beta.orig)
summary.beta <- t(apply(samples.beta.orig, 2, quantile, c(0.5, 0.025, 0.975))) 
summary.beta <- cbind(summary.beta, rep(n.keep, p), rep(accept.beta,p), effectiveSize(samples.beta.orig), geweke.diag(samples.beta.orig)$z)
rownames(summary.beta) <- colnames(X)
colnames(summary.beta) <- c("Median", "2.5%", "97.5%", "n.sample", "% accept", "n.effective", "Geweke.diag")

summary.hyper <- array(NA, c(2,7))
summary.hyper[1, 1:3] <- quantile(samples.tau2, c(0.5, 0.025, 0.975))
summary.hyper[1, 4:7] <- c(n.keep, accept.tau2, effectiveSize(samples.tau2), geweke.diag(samples.tau2)$z)
summary.hyper[2, 1:3] <- quantile(samples.sigma2, c(0.5, 0.025, 0.975))
summary.hyper[2, 4:7] <- c(n.keep, accept.sigma2, effectiveSize(samples.sigma2), geweke.diag(samples.sigma2)$z)

summary.results <- rbind(summary.beta, summary.hyper)
rownames(summary.results)[(nrow(summary.results)-1):(nrow(summary.results))] <- c("tau2", "sigma2")
summary.results[ , 1:3] <- round(summary.results[ , 1:3], 4)
summary.results[ , 4:7] <- round(summary.results[ , 4:7], 1)


#### Create the fitted values and residuals
fitted.values <- apply(samples.fitted, 2, mean)
response.residuals <- as.numeric(Y) - fitted.values
pearson.residuals <- response.residuals /sqrt(fitted.values * (1 - mean.prob))
residuals <- data.frame(response=response.residuals, pearson=pearson.residuals)


#### Compile and return the results
model.string <- c("Likelihood model - Binomial (logit link function)", "\nRandom effects model - BYM CAR\n")
if(n.miss==0) samples.Y = NA

samples <- list(beta=samples.beta.orig, psi=mcmc(samples.re), tau2=mcmc(samples.tau2), sigma2=mcmc(samples.sigma2), fitted=mcmc(samples.fitted), Y=mcmc(samples.Y))
results <- list(summary.results=summary.results, samples=samples, fitted.values=fitted.values, residuals=residuals, modelfit=modelfit, accept=accept.final, localised.structure=NULL,  formula=formula, model=model.string, X=X)
class(results) <- "CARBayes"


#### Finish by stating the time taken    
    if(verbose)
    {
    b<-proc.time()
    cat("Finished in ", round(b[3]-a[3], 1), "seconds.\n")
    }else
    {}
return(results)
}

