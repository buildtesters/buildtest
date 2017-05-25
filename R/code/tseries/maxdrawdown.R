library(tseries)
# Toy example
x <- c(1:10, 9:7, 8:14, 13:8, 9:20)
mdd <- maxdrawdown(x)
mdd
plot(x)
segments(mdd$from, x[mdd$from], mdd$to, x[mdd$from], col="grey")
segments(mdd$from, x[mdd$to], mdd$to, x[mdd$to], col="grey")
mid <- (mdd$from + mdd$to)/2
arrows(mid, x[mdd$from], mid, x[mdd$to], col="red", length = 0.16)
# Realistic example
data(EuStockMarkets)
dax <- log(EuStockMarkets[,"DAX"])
mdd <- maxdrawdown(dax)
mdd
plot(dax)
segments(time(dax)[mdd$from], dax[mdd$from],
time(dax)[mdd$to], dax[mdd$from], col="grey")
segments(time(dax)[mdd$from], dax[mdd$to],
time(dax)[mdd$to], dax[mdd$to], col="grey")
mid <- time(dax)[(mdd$from + mdd$to)/2]
arrows(mid, dax[mdd$from], mid, dax[mdd$to], col="red", length = 0.16)
