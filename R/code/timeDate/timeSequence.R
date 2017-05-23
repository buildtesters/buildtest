library(timeDate)
## timeSequence -
## autodetection of format :
(t1 <- timeSequence(from = "2004-03-12", to = "2004-04-11"))
stopifnot( ## different formats even:
identical(t1, timeSequence(from = "2004-03-12", to = "11-Apr-2004")),
identical(t1, ## explicit format and FinCenter :
timeSequence(from = "2004-03-12", to = "2004-04-11",
format = "%Y-%m-%d", FinCenter = "GMT")))
## observe "switch to summer time":
timeSequence(from = "2004-03-12", to = "2004-04-11",
FinCenter = "Europe/Zurich")
