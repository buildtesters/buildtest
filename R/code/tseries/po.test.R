library(tseries)
x <- ts(diffinv(matrix(rnorm(2000),1000,2))) # no cointegration
po.test(x)
x <- diffinv(rnorm(1000))
y <- 2.0-3.0*x+rnorm(x,sd=5)
z <- ts(cbind(x,y)) # cointegrated
po.test(z)
