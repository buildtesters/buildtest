# https://cran.r-project.org/web/packages/assertthat/assertthat.pdf
library(assertthat)
x <- 2
see_if(are_equal(x, 1.9))
see_if(are_equal(x, 1.999, tol = 0.01))
see_if(are_equal(x, 2))
