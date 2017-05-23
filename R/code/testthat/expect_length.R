library(testthat)
expect_length(1, 1)
expect_length(1:10, 10)
## Not run:
expect_length(1:10, 1)
## End(Not run)
