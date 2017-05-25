library(tibble)
lst(n = 5, x = runif(n))
# You can splice-unquote a list of quotes and formulas
lst(!!! list(n = rlang::quo(2 + 3), y = quote(runif(n))))
a <- 1:5
tibble(a, b = a * 2)
tibble(a, b = a * 2, c = 1)
tibble(x = runif(10), y = x * 2)
lst(n = 5, x = runif(n))
# tibble never coerces its inputs
str(tibble(letters))
str(tibble(x = list(diag(1), diag(2))))
# or munges column names
tibble(`a + b` = 1:5)
# You can splice-unquote a list of quotes and formulas
tibble(!!! list(x = rlang::quo(1:10), y = quote(x * 2)))
# data frames can only contain 1d atomic vectors and lists
# and can not contain POSIXlt
## Not run:
tibble(x = tibble(1, 2, 3))
tibble(y = strptime("2000/01/01", "%x"))
## End(Not run)

