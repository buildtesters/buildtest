# https://stat.ethz.ch/R-manual/R-devel/library/base/html/any.html
range(x <- sort(round(stats::rnorm(10) - 1.2, 1)))
if(any(x < 0)) cat("x contains negative values\n")
