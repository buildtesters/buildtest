library(tseries)
x <- rnorm(1000)
dim(x) <- c(500,2)
res <- portfolio.optim(x)
res$pw
require("zoo") # For diff() method.
X <- diff(log(as.zoo(EuStockMarkets)))
res <- portfolio.optim(X) ## Long only
res$pw
res <- portfolio.optim(X, shorts=TRUE) ## Long/Short
res$pw
