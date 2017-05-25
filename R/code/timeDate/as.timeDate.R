# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## timeDate -
tC = timeCalendar()
## Convert 'timeDate' to a character strings:
as.character(tC)
## Coerce a 'Date' object into a 'timeDate' object:
as.timeDate(Sys.Date())

