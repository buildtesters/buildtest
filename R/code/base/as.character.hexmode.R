# https://stat.ethz.ch/R-manual/R-devel/library/base/html/hexmode.html
i <- as.hexmode("7fffffff")
i; class(i)
identical(as.integer(i), .Machine$integer.max)

hm <- as.hexmode(c(NA, 1)); hm
as.integer(hm)
