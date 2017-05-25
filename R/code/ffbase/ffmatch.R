# https://cran.r-project.org/web/packages/ffbase/ffbase.pdf 
## Basic example of match.ff
library(ffbase)
x.ff <- ffmatch( as.ff(as.factor(c(LETTERS, NA)))
, as.ff(as.factor(c("C","B","Z","X","HMM","Nothing",NA)))
, trace=TRUE
, BATCHBYTES=20)
class(x.ff)
x <- match(c(LETTERS, NA), c("C","B","Z","X","HMM","Nothing",NA))
table(x.ff[] == x, exclude=c())
## ffdfmatch also allows to input an ffdf
data(iris)
ffiris <- as.ffdf(iris)
ffirissubset <- as.ffdf(iris[c(1:10, nrow(iris)), ])
ffdfmatch(ffiris, ffirissubset, trace=TRUE, BATCHBYTES=500)
## %in% is masked from the base package
letter <- factor(c(LETTERS, NA))
check <- factor(c("C","B","Z","X","HMM","Nothing",NA))
letter %in% check
as.ff(letter) %in% as.ff(check)
ffiris %in% ffirissubset

