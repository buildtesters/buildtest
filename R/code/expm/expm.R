# https://cran.r-project.org/web/packages/expm/expm.pdf
library(expm)
source(system.file("demo", "exact-fn.R", package = "expm"))
##-> rnilMat() ; xct10
set.seed(1)
(s5 <- Matrix(m5 <- rnilMat(5))); v <- c(1,6:9)
(em5 <- expm(m5))
r5 <- expAtv(m5, v)
r5. <- expAtv(s5, v)
stopifnot(all.equal(r5, r5., tolerance = 1e-14),
all.equal(c(em5 %*% v), r5$eAtv))
v <- 10:1
with(xct10, all.equal(expm(m), expm))
all.equal(c(xct10$expm %*% v),
expAtv(xct10$m, v)$eAtv)

