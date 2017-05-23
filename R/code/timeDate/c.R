# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## timeCalendar -
# Create Character Vectors:
GMT = timeCalendar(zone = "GMT", FinCenter = "GMT") + 16*3600
ZUR = timeCalendar(zone = "GMT", FinCenter = "Zurich") + 16*3600
## c -
# Concatenate and Replicate timeDate Objects:
sort(c(GMT, ZUR))
sort(c(ZUR, GMT))
