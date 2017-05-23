library(tibble)
glimpse(mtcars)
if (!requireNamespace("nycflights13", quietly = TRUE))
stop("Please install the nycflights13 package to run the rest of this example")
glimpse(nycflights13::flights)

