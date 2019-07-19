# This is the function that will perform the sampling of the CAR model.

CompleteCarSampler = function(X.standardised, K, p, beta, Y.DA, 
                              trials, prior.mean.beta, prior.var.beta, 
                              n.beta.block, proposal.sd.beta, list.block, Wtriplet, 
                              Wbegfin, Wtripletsum, phi, tau2, proposal.sd.phi,
                              theta,sigma2, proposal.sd.theta,accept.all,iter_index) {
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
    #### Why substract mean of islands
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
    ### Same thing, substracting theta
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
    ## The model written form
    lp <- as.numeric(X.standardised %*% beta) + phi + theta + offset
    prob <- exp(lp)  / (1 + exp(lp))
    fitted <- trials * prob
    loglike <- dbinom(x=Y, size=trials, prob=prob, log=TRUE)


    

    
    ########################################
    ## Self tune the acceptance probabilties
    ########################################
    k <- iter_index/100
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
        print(proposal.sd.beta)
        }else
        {   
        }
    
    
  exports  <- list(beta = beta,
                   phi = phi,
                   theta = theta,
                   re = samples.re,
                   tau2 = tau2,
                   sigma2 = sigma2,
                   loglike = loglike,
                   fitted = fitted,
                   Y.DA = Y.DA,
                   proposal.sd.phi = proposal.sd.phi,
                   proposal.sd.theta = proposal.sd.theta,
                   proposal.sd.beta = proposal.sd.beta,
                   accept.all = accept.all)
  return(exports)
} 
