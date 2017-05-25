library(timeDate)
## Date as character String:
charvec = "2006-04-16"
## timeNdayOnOrAfter
# What date has the first Monday on or after March 15, 1986 ?
timeNdayOnOrAfter("1986-03-15", 1)
## timeNdayOnOrBefore
# What date has Friday on or before April 22, 1977 ?
timeNdayOnOrBefore("1986-03-15", 5)
