library(tseries)
x <- rnorm(1000) # no unit-root
adf.test(x)
y <- diffinv(x) # contains a unit-root
adf.test(y)
