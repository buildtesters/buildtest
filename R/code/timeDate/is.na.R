library(timeDate)
# Create a timeCalendar sequence
(td <- timeCalendar())
is.na(td)
# insert NA's
is.na(td) <- 2:3
td
# test of NA's
is.na(td)

