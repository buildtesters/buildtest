library(tseries)
n <- 10
t <- cumsum(rexp(n, rate = 0.1))
v <- rnorm(n)
x <- irts(t, v)
daysecond(x)
weekday(x)
is.businessday(x)
is.weekend(x)
x
approx.irts(x, seq(ISOdatetime(1970, 1, 1, 0, 0, 0, tz = "GMT"),
by = "10 secs", length = 7), rule = 2)
## Not run:
file <- tempfile()
# To write an irregular time-series object to a file one might use
write.irts(x, file = file)
# To read an irregular time-series object from a file one might use
read.irts(file = file)
unlink(file)
## End(Not run)

