library(TH.data)
data(GBSG2)
thsum <- function(x) {
ret <- c(median(x), quantile(x, 0.25), quantile(x,0.75))
names(ret)[1] <- "Median"
ret
}
t(apply(GBSG2[,c("age", "tsize", "pnodes",
"progrec", "estrec")], 2, thsum))
table(GBSG2$menostat)
table(GBSG2$tgrade)
table(GBSG2$horTh)
