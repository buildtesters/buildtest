# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
date <- timeDate("2008-01-01")
finCenter(date) <- "GMT"
date
finCenter(date) <- "Zurich"
date

