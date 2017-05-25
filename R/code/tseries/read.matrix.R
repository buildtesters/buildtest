library(tseries)
x <- matrix(0, 10, 10)
write(x, "test", ncolumns=10)
x <- read.matrix("test")
x
unlink("test")
