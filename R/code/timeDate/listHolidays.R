# https://cran.r-project.org/web/packages/timeDate/timeDate.pdf
library(timeDate)
## listHolidays -
listHolidays()
## CHSechselaeuten -
# Sechselaeuten a half Day Bank Holiday in Switzerland
CHSechselaeuten(2000:2010)
CHSechselaeuten(getRmetricsOptions("currentYear"))
## German Unification Day:
DEGermanUnity(getRmetricsOptions("currentYear"))
