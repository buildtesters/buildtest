library(testthat)
a <- 9
expect_lt(a, 10)
## Not run:
expect_lt(11, 10)
## End(Not run)
a <- 11
expect_gt(a, 10)
## Not run:
expect_gt(9, 10)
## End(Not run)
