library(tidyr)
## align -
# Align Bi-Weekly with a 3 Days Offset:
(tC <- timeCalendar())
align(tC, by = "2w", offset = "3d")
## alignDaily -
# Simple to use Functions:
alignDaily(tC)
alignDaily(tC, include.weekends=TRUE)
# Align to end-of-month Dates:
alignMonthly(tC)
