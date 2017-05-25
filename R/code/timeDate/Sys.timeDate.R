library(timeDate)
## Sys.time -
# direct
Sys.timeDate()
# transformed from "POSIX(c)t"
timeDate(Sys.time())
# Local Time in Zurich
timeDate(Sys.time(), FinCenter = "Zurich")
