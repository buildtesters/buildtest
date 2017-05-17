# https://stat.ethz.ch/R-manual/R-devel/library/base/html/allnames.html
all.names(expression(sin(x+y)))
all.names(quote(sin(x+y))) # or a call
all.vars(expression(sin(x+y)))
