# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
# Date and Time Now:
now = Sys.timeDate()
# One Hour Later:
now + 3600
# Which date/time is earlier or later ?
tC = timeCalendar()
tR = tC + round(3600*rnorm(12))
tR > tC
