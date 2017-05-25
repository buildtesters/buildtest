# https://cran.r-project.org/web/packages/Brobdingnag/Brobdingnag.pdf
library(Brobdingnag)
x <- as.brob(1:10)
y <- 1e10
x+y
as.numeric((x+y)-1e10)
x^(1/y)
