# https://cran.r-project.org/web/packages/foreign/foreign.pdf
library(foreign)
x <- read.dbf(system.file("files/sids.dbf", package="foreign")[1])
str(x)
summary(x)

