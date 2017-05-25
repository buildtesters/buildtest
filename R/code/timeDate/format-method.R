# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## timeCalendar -
# Time Calebdar 16:00
tC = timeCalendar() + 16*3600
tC
## Format as ISO Character String:
format(tC)
