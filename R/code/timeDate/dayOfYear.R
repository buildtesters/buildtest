# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## timeCalendat -
tC = timeCalendar()
## The days of the Year:
dayOfYear(tC)
## Use Deprecated Function:
getDayOfYear <- dayOfYear
getDayOfYear(tC)
