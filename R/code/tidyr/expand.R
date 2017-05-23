# https://cran.r-project.org/web/packages/tidyr/tidyr.pdf
library(tidyr)
library(dplyr)
# All possible combinations of vs & cyl, even those that aren't
# present in the data
expand(mtcars, vs, cyl)
# Only combinations of vs and cyl that appear in the data
expand(mtcars, nesting(vs, cyl))
# Implicit missings ---------------------------------------------------------
df <- data_frame(
year = c(2010, 2010, 2010, 2010, 2012, 2012, 2012),
qtr = c( 1, 2, 3, 4, 1, 2, 3),
return = rnorm(7)
)
df %>% expand(year, qtr)
df %>% expand(year = 2010:2012, qtr)
df %>% expand(year = full_seq(year, 1), qtr)
df %>% complete(year = full_seq(year, 1), qtr)
# Nesting -------------------------------------------------------------------
# Each person was given one of two treatments, repeated three times
# But some of the replications haven't happened yet, so we have
# incomplete data:
experiment <- data_frame(
name = rep(c("Alex", "Robert", "Sam"), c(3, 2, 1)),
trt = rep(c("a", "b", "a"), c(3, 2, 1)),
rep = c(1, 2, 3, 1, 2, 1),
measurment_1 = runif(6),
measurment_2 = runif(6)
)
# We can figure out the complete set of data with expand()
# Each person only gets one treatment, so we nest name and trt together:
all <- experiment %>% expand(nesting(name, trt), rep)
all
# We can use anti_join to figure out which observations are missing
all %>% anti_join(experiment)
# And use right_join to add in the appropriate missing values to the
# original data
experiment %>% right_join(all)
# Or use the complete() short-hand
experiment %>% complete(nesting(name, trt), rep)

