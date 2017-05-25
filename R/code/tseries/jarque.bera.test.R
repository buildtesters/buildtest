library(tseries)
x <- rnorm(100) # null
jarque.bera.test(x)
x <- runif(100) # alternative
jarque.bera.test(x)

