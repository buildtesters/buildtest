library(tseries)
n <- 10
t <- cumsum(rexp(n, rate = 0.1))
v <- rnorm(n)
x <- irts(t, v)
x
time(x)
value(x)
plot(x)
points(x)
t <- cumsum(c(t[1], rexp(n-1, rate = 0.2)))
v <- rnorm(n, sd = 0.1)
x <- irts(t, v)
lines(x, col = "red")
points(x, col = "red")
# Multivariate
t <- cumsum(rexp(n, rate = 0.1))
u <- rnorm(n)
v <- rnorm(n)
x <- irts(t, cbind(u, v))
x
x[,1]
x[1:3,]
x[1:3,1]
plot(x)
