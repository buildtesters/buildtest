# https://cran.r-project.org/web/packages/calibrate/calibrate.pdf
library(calibrate)
x <- rnorm(20,1)
y <- rnorm(20,1)
x <- x - mean(x)
y <- y - mean(y)
z <- x + y
b <- c(1,1)
plot(x,y,asp=1,pch=19)
tm<-seq(-2,2,by=0.5)
Calibrate.z <- calibrate(b,z,tm,cbind(x,y),axislab="Z",graphics=TRUE)

