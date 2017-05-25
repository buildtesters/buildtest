library(gam)
data(gam.data)
gam.object <- gam(y ~ s(x,6) + z,data=gam.data)
plot(gam.object,se=TRUE)
data(gam.newdata)
preplot(gam.object,newdata=gam.newdata)

