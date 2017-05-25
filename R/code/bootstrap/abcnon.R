# https://cran.r-project.org/web/packages/bootstrap/bootstrap.pdf
library(bootstrap)
# compute abc intervals for the mean
x <- rnorm(10)
theta <- function(p,x) {sum(p*x)/sum(p)}
results <- abcnon(x, theta)
# compute abc intervals for the correlation
x <- matrix(rnorm(20),ncol=2)
theta <- function(p, x)
{
x1m <- sum(p * x[, 1])/sum(p)
x2m <- sum(p * x[, 2])/sum(p)
num <- sum(p * (x[, 1] - x1m) * (x[, 2] - x2m))
den <- sqrt(sum(p * (x[, 1] - x1m)^2) *
sum(p * (x[, 2] - x2m)^2))
return(num/den)
}
results <- abcnon(x, theta)

