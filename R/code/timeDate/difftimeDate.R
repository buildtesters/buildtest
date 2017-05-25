# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## Create Character Vectors:
dts = c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
dts
## timeDate -
GMT = timeDate(dts, zone = "GMT", FinCenter = "GMT")
GMT
## diff -
# Suitably Lagged and Iterated Differences:
difftimeDate(GMT[1:2], GMT[-(1:2)])
