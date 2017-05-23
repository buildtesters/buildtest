# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## holiday -
# Dates for GoodFriday from 2000 until 2010:
holiday(2000:2010, "GoodFriday")
## Easter -
Easter(2000:2010)
## GoodFriday -
GoodFriday(2000:2010)
Easter(2000:2010, -2)
