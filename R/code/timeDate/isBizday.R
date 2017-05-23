library(timeDate)
## Dates in April, currentYear:
currentYear = getRmetricsOptions("currentYear")
tS = timeSequence(
from = paste(currentYear, "-03-01", sep = ""),
to = paste(currentYear, "-04-30", sep = ""))
tS
## Subset Business Days at NYSE:
holidayNYSE()
isBizday(tS, holidayNYSE())
tS[isBizday(tS, holidayNYSE())]
