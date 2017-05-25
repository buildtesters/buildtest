library(gam)
data(gam.data)
gam(y ~ s(x) + z, data=gam.data)

