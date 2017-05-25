library(gam)
data(gam.data)
gam.object <- gam(y~x+z, data=gam.data)
step.object <-step.gam(gam.object, scope=list("x"=~1+x+s(x,4)+s(x,6)+s(x,12),"z"=~1+z+s(z,4)))
## Not run:
# Parallel
require(doMC)
registerDoMC(cores=2)
step.gam(gam.object, scope=list("x"=~1+x+s(x,4)+s(x,6)+s(x,12),"z"=~1+z+s(z,4)),parallel=TRUE)
## End(Not run)
