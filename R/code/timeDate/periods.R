library(timeDate)
## Create Time Sequence -
x <- timeSequence(from = "2001-01-01", to = "2009-01-01", by = "day")
## Generate Periods -
periods(x, "12m", "1m")
periods(x, "52w", "4w")
## Roll Periodically -
periodicallyRolling(x)
## Roll Monthly -
monthlyRolling(x)
