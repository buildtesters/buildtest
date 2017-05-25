# https://cran.r-project.org/web/packages/ff/ff.pdf
library(ff)
d <- data.frame(a=letters, b=rev(letters), c=1:26)
x <- as.ffdf(d)
d[1,]
x[1,]
d[1:2,]
x[1:2,]
d[,1]
x[,1]
d[,1:2]
x[,1:2]
d[cbind(1:2,2:1)]
x[cbind(1:2,2:1)]
d[1]
x[1]
d[[1]]
x[[1]]
d$a
x$a
d$a[1:2]
x$a[1:2]
rm(x); gc()
