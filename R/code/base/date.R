# https://stat.ethz.ch/R-manual/R-devel/library/base/html/date.html
(d <- date())
nchar(d) == 24

## something similar in the current locale
format(Sys.time(), "%a %b %d %H:%M:%S %Y")

