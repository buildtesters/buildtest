# https://cran.r-project.org/web/packages/EasyABC/EasyABC.pdf 
## the model is a C++ function packed into a R function -- the option 'use_seed'
## must be turned to TRUE.
library(EasyABC)
trait_prior=list(c("unif",3,5),c("unif",-2.3,1.6),c("unif",-25,125),c("unif",-0.7,3.2))
trait_prior
## only launching simulations with parameters drawn in the prior distributions
ABC_emul = ABC_emulation(model=trait_model, prior=trait_prior,
nb_design_pts=10, nb_simul=300, use_seed=TRUE, progress=TRUE)
ABC_emul
## launching simulations with parameters drawn in the prior distributions and performing
# the rejection step
sum_stat_obs=c(100,2.5,20,30000)
ABC_emul = ABC_emulation(model=trait_model, prior=trait_prior, tol=0.2, nb_design_pts=10,
nb_simul=100, summary_stat_target=sum_stat_obs, use_seed=TRUE, progress=TRUE)
ABC_emul

