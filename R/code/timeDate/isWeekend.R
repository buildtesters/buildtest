library(timeDate)
## Dates in April, currentYear:
currentYear = getRmetricsOptions("currentYear")
tS = timeSequence(
from = paste(currentYear, "-03-01", sep = ""),
to = paste(currentYear, "-04-30", sep = ""))
tS
## Subset of Weekends:
isWeekend(tS)
tS[isWeekend(tS)]
