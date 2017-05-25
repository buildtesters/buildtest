# https://cran.r-project.org/web/packages/testthat/testthat.pdf
library(testthat)
# Character -----------------------------------------------------------------
x <- c("abc", "def", "jih")
compare(x, x)
y <- paste0(x, "y")
compare(x, y)
compare(letters, paste0(letters, "-"))
x <- "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis cursus
tincidunt auctor. Vestibulum ac metus bibendum, facilisis nisi non, pulvinar
dolor. Donec pretium iaculis nulla, ut interdum sapien ultricies a. "
y <- "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis cursus
tincidunt auctor. Vestibulum ac metus1 bibendum, facilisis nisi non, pulvinar
dolor. Donec pretium iaculis nulla, ut interdum sapien ultricies a. "
compare(x, y)
compare(c(x, x), c(y, y))
# Numeric -------------------------------------------------------------------
x <- y <- runif(100)
y[sample(100, 10)] <- 5
compare(x, y)
x <- y <- 1:10
x[5] <- NA
x[6] <- 6.5
compare(x, y)
# Compare ignores minor numeric differences in the same way
# as all.equal.
compare(x, x + 1e-9)

