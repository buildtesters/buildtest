library(tseries)
x <- rnorm(1000) # is level stationary
kpss.test(x)
y <- cumsum(x) # has unit root
kpss.test(y)
x <- 0.3*(1:1000)+rnorm(1000) # is trend stationary
kpss.test(x, null = "Trend")
