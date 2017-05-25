# https://cran.r-project.org/web/packages/futile.options/futile.options.pdf
library(futile.options)
my.options <- OptionsManager('my.options', defaults=list(a=1,b=2))
my.options(a=5, c=3)
my.options('a')
