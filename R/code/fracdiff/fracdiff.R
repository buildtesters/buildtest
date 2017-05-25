# https://cran.r-project.org/web/packages/fracdiff/fracdiff.pdf
library(fracdiff)
ts.test <- fracdiff.sim( 5000, ar = .2, ma = -.4, d = .3)
fd. <- fracdiff( ts.test$series,
nar = length(ts.test$ar), nma = length(ts.test$ma))
fd.
## Confidence intervals
confint(fd.)
## with iteration output
fd2 <- fracdiff(ts.test$series, nar = 1, nma = 1, trace = 1)
all.equal(fd., fd2)

