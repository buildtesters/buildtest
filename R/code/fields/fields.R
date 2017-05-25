# https://cran.r-project.org/web/packages/fields/fields.pdf
library(fields)
# some air quality data, daily surface ozone measurements for the Midwest:
data(ozone2)
x<-ozone2$lon.lat
y<- ozone2$y[16,] # June 18, 1987
# pixel plot of spatial data
quilt.plot( x,y)
US( add=TRUE) # add US map
fit<- Tps(x,y)
# fits a GCV thin plate smoothing spline surface to ozone measurements.
# Hey, it does not get any easier than this!
summary(fit) #diagnostic summary of the fit
set.panel(2,2)
plot(fit) # four diagnostic plots of fit and residuals.
# quick plot of predicted surface
set.panel()
surface(fit) # contour/image plot of the fitted surface
US( add=TRUE, col="magenta", lwd=2) # US map overlaid
title("Daily max 8 hour ozone in PPB, June 18th, 1987")
fit2<- spatialProcess( x,y)
# a "Kriging" model. The covariance defaults to a Matern with smoothness 1.0.
# the nugget, sill and range parameters are found by maximum likelihood
# summary, plot, and surface also work for fit2 !
