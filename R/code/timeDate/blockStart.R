# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## timeSequence
# 360 Days Series:
tS <- timeSequence(length.out = 360)
## blockStart | blockEnd -
Start <- blockStart(tS, 30)
End <- blockEnd(tS, 30)
Start
End
End-Start
