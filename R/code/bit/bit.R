# https://cran.r-project.org/web/packages/bit/bit.pdf
library(bit)
x <- bit(12) # create bit vector
x # autoprint bit vector
length(x) <- 16 # change length
length(x) # get length
x[[2]] # extract single element
x[[2]] <- TRUE # replace single element
x[1:2] # extract parts of bit vector
x[1:2] <- TRUE # replace parts of bit vector
as.which(x) # coerce bit to subscripts
x <- as.bit.which(3:4, 4) # coerce subscripts to bit
as.logical(x) # coerce bit to logical
y <- as.bit(c(FALSE, TRUE, FALSE, TRUE)) # coerce logical to bit
is.bit(y) # test for bit
!x # boolean NOT
x & y # boolean AND
x | y # boolean OR
xor(x, y) # boolean Exclusive OR
x != y # boolean unequality (same as xor)
x == y # boolean equality
all(x) # aggregate AND
any(x) # aggregate OR
min(x) # aggregate MIN (integer version of ALL)
max(x) # aggregate MAX (integer version of ANY)
range(x) # aggregate [MIN,MAX]
sum(x) # aggregate SUM (count of TRUE)
summary(x) # aggregate count of FALSE and TRUE
## Not run:
message("\nEven for a single boolean operation transforming logical to bit pays off")
n <- 10000000
x <- sample(c(FALSE, TRUE), n, TRUE)
y <- sample(c(FALSE, TRUE), n, TRUE)
system.time(x|y)
system.time({
x <- as.bit(x)
y <- as.bit(y)
})
system.time( z <- x | y )
system.time( as.logical(z) )
message("Even more so if multiple operations are needed :-)")
message("\nEven for a single set operation transforming subscripts to bit pays off\n")
n <- 10000000
x <- sample(n, n/2)
y <- sample(n, n/2)
system.time( union(x,y) )
system.time({
x <- as.bit.which(x, n)
y <- as.bit.which(y, n)
})
system.time( as.which.bit( x | y ) )
message("Even more so if multiple operations are needed :-)")
message("\nSome timings WITH memory allocation")
n <- 2000000
l <- sample(c(FALSE, TRUE), n, TRUE)
# copy logical to logical
system.time(for(i in 1:100){ # 0.0112
l2 <- l
l2[1] <- TRUE # force new memory allocation (copy on modify)
rm(l2)
})/100
# copy logical to bit
system.time(for(i in 1:100){ # 0.0123
b <- as.bit(l)
rm(b)
})/100
# copy bit to logical
b <- as.bit(l)
system.time(for(i in 1:100){ # 0.009
l2 <- as.logical(b)
rm(l2)
})/100
# copy bit to bit
b <- as.bit(l)
system.time(for(i in 1:100){ # 0.009
b2 <- b
b2[1] <- TRUE # force new memory allocation (copy on modify)
rm(b2)
})/100
l2 <- l
# replace logical by TRUE
system.time(for(i in 1:100){
l[] <- TRUE
})/100
# replace bit by TRUE (NOTE that we recycle the assignment
# value on R side == memory allocation and assignment first)
system.time(for(i in 1:100){
b[] <- TRUE
})/100
# THUS the following is faster
system.time(for(i in 1:100){
b <- !bit(n)
})/100
# replace logical by logical
system.time(for(i in 1:100){
l[] <- l2
})/100
# replace bit by logical
system.time(for(i in 1:100){
b[] <- l2
})/100
# extract logical
system.time(for(i in 1:100){
l2[]
})/100
# extract bit
system.time(for(i in 1:100){
b[]
})/100
message("\nSome timings WITHOUT memory allocation (Serge, that's for you)")
n <- 2000000L
l <- sample(c(FALSE, TRUE), n, TRUE)
b <- as.bit(l)
# read from logical, write to logical
l2 <- logical(n)
system.time(for(i in 1:100).Call("R_filter_getset", l, l2, PACKAGE="bit")) / 100
# read from bit, write to logical
l2 <- logical(n)
system.time(for(i in 1:100).Call("R_bit_get", b, l2, c(1L, n), PACKAGE="bit")) / 100
# read from logical, write to bit
system.time(for(i in 1:100).Call("R_bit_set", b, l2, c(1L, n), PACKAGE="bit")) / 100

