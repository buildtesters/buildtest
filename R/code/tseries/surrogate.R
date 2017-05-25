library(tseries)
x <- 1:10 # Simple example
surrogate(x)
n <- 500 # Generate AR(1) process
e <- rnorm(n)
x <- double(n)
x[1] <- rnorm(1)
for(i in 2:n) {
x[i] <- 0.4 * x[i-1] + e[i]
}
x <- ts(x)
theta <- function(x) # Autocorrelations up to lag 10
return(acf(x, plot=FALSE)$acf[2:11])
surrogate(x, ns=50, fft=TRUE, statistic=theta)

