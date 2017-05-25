library(gam)
data(gam.data)
gam.object <- gam(y ~ s(x,6) + z, data=gam.data)
predict(gam.object) # extract the additive predictors
data(gam.newdata)
predict(gam.object, gam.newdata, type="terms")
