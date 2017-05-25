library(tseries)
n <- 500 # Generate AR(1) process
a <- 0.6
e <- rnorm(n+100)
x <- double(n+100)
x[1] <- rnorm(1)
for(i in 2:(n+100)) {
x[i] <- a * x[i-1] + e[i]
}
x <- ts(x[-(1:100)])
tsbootstrap(x, nb=500, statistic=mean)
# Asymptotic formula for the std. error of the mean
sqrt(1/(n*(1-a)^2))
acflag1 <- function(x)
{
xo <- c(x[,1], x[1,2])
xm <- mean(xo)
return(mean((x[,1]-xm)*(x[,2]-xm))/mean((xo-xm)^2))
}
tsbootstrap(x, nb=500, statistic=acflag1, m=2)
# Asymptotic formula for the std. error of the acf at lag one
sqrt(((1+a^2)-2*a^2)/n)
