# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## Create Character Vectors:
dts = c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
dts
tms = c( "23:12:55", "10:34:02", "08:30:00", "11:18:23")
tms
## timeDate -
GMT = timeDate(dts, zone = "GMT", FinCenter = "GMT") + 24*3600
GMT
ZUR = timeDate(dts, zone = "GMT", FinCenter = "Europe/Zurich")
ZUR
## diff -
# Suitably Lagged and Iterated Differences:
diff(GMT)
diff(GMT, lag = 2)
diff(GMT, lag = 1, diff = 2)
