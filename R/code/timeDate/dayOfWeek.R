# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## timeCalendat -
tC = timeCalendar()
## The days of the Year:
dayOfWeek(tC)
## Use Deprecated Function:
getDayOfWeek <- dayOfWeek
getDayOfWeek(tC)
