# https://cran.r-project.org/web/packages/fail/fail.pdf
library(fail)
# initialize a FAIL in a temporary directory
path <- tempfile("")
files <- fail(path)
# save x and y, vectors of random numbers
x <- runif(100)
files$put(x, y = runif(100))
# save columns of the iris data set as separate files
files$put(li = as.list(iris))
# load all RData files in a named list as a one-liner
as.list(fail(path))
# load a single object from the file system
files$get("Species")
files$as.list(c("x", "y"))
# remove an object (and related file)
files$remove("Species")
# apply a function over files
files$apply(mean)
files$mapply(function(key, value) sprintf("%s -> %f", key, mean(value)), simplify = TRUE)
# show file size informations
files$size(unit = "Mb")
# get an object and cache it
files$get("x", use.cache = TRUE)
files$cached()
files$clear()
files$cached()
# assign variables in the current environment
files$assign("y")
mean(y)

