library(tseries)
x <- rnorm(1000) # no unit-root
pp.test(x)
y <- cumsum(x) # has unit root
pp.test(y)

