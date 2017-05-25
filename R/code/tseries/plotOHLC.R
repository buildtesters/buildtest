library(tseries)
con <- url("https://finance.yahoo.com")
if(!inherits(try(open(con), silent = TRUE), "try-error")) {
close(con)
## Plot OHLC bar chart for the last 'nDays' days of the instrument
## 'instrument'
nDays <- 50
instrument <- "^gspc"
start <- strftime(as.POSIXlt(Sys.time() - nDays * 24 * 3600),
format="%Y-%m-%d")
end <- strftime(as.POSIXlt(Sys.time()), format = "%Y-%m-%d")
x <- get.hist.quote(instrument = instrument, start = start, end = end,
retclass = "ts")
plotOHLC(x, ylab = "price", main = instrument)
}
