# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## Date as character String:
charvec = "2006-04-16"
myFinCenter = getRmetricsOptions("myFinCenter")
## timeLastDayInMonth-
# What date has the last day in a month for a given date ?
timeLastDayInMonth(charvec, format = "%Y-%m-%d",
zone = myFinCenter, FinCenter = myFinCenter)
timeLastDayInMonth(charvec)
timeLastDayInMonth(charvec, FinCenter = "Zurich")
## timeFirstDayInMonth -
# What date has the first day in a month for a given date ?
timeFirstDayInMonth(charvec)
## timeLastDayInQuarter -
# What date has the last day in a quarter for a given date ?
timeLastDayInQuarter(charvec)
## timeFirstDayInQuarter -
# What date has the first day in a quarter for a given date ?
timeFirstDayInQuarter(charvec)
## timeNdayOnOrAfter
# What date has the first Monday on or after March 15, 1986 ?
timeNdayOnOrAfter("1986-03-15", 1)
## timeNdayOnOrBefore
# What date has Friday on or before April 22, 1977 ?
timeNdayOnOrBefore("1986-03-15", 5)
## timeNthNdayInMonth -
# What date is the second Monday in April 2004 ?
timeNthNdayInMonth("2004-04-01", 1, 2)
## timeLastNdayInMonth -
# What date has the last Tuesday in May, 1996 ?
timeLastNdayInMonth("1996-05-01", 2)
