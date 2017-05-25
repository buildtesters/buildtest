# https://cran.r-project.org/web/packages/foreach/foreach.pdf
library(foreach)
# equivalent to rnorm(3)
times(3) %do% rnorm(1)
# equivalent to lapply(1:3, sqrt)
foreach(i=1:3) %do%
sqrt(i)
# equivalent to colMeans(m)
m <- matrix(rnorm(9), 3, 3)
foreach(i=1:ncol(m), .combine=c) %do%
mean(m[,i])
# normalize the rows of a matrix in parallel, with parenthesis used to
# force proper operator precedence
# Need to register a parallel backend before this example will run
# in parallel
foreach(i=1:nrow(m), .combine=rbind) %dopar%
(m[i,] / mean(m[i,]))
# simple (and inefficient) parallel matrix multiply
library(iterators)
a <- matrix(1:16, 4, 4)
b <- t(a)
foreach(b=iter(b, by='col'), .combine=cbind) %dopar%
(a %*% b)
# split a data frame by row, and put them back together again without
# changing anything
d <- data.frame(x=1:10, y=rnorm(10))
s <- foreach(d=iter(d, by='row'), .combine=rbind) %dopar% d
identical(s, d)
# a quick sort function
qsort <- function(x) {
n <- length(x)
if (n == 0) {
x
} else {
p <- sample(n, 1)
smaller <- foreach(y=x[-p], .combine=c) %:% when(y <= x[p]) %do% y
larger <- foreach(y=x[-p], .combine=c) %:% when(y > x[p]) %do% y
c(qsort(smaller), x[p], qsort(larger))
}
}
qsort(runif(12))
