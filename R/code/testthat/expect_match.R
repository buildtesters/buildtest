library(testthat)
expect_match("Testing is fun", "fun")
expect_match("Testing is fun", "f.n")
## Not run:
expect_match("Testing is fun", "horrible")
# Zero-length inputs always fail
expect_match(character(), ".")
## End(Not run)
