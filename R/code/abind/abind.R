# https://cran.r-project.org/web/packages/abind/abind.pdf

library(abind)
# Five different ways of binding together two matrices
x <- matrix(1:12,3,4)
y <- x+100
dim(abind(x,y,along=0)) # binds on new dimension before first
dim(abind(x,y,along=1)) # binds on first dimension
dim(abind(x,y,along=1.5))
dim(abind(x,y,along=2))
dim(abind(x,y,along=3))
dim(abind(x,y,rev.along=1)) # binds on last dimension
dim(abind(x,y,rev.along=0)) # binds on new dimension after last
# Unlike cbind or rbind in that the default is to bind
# along the last dimension of the inputs, which for vectors
# means the result is a vector (because a vector is
# treated as an array with length(dim(x))==1).
abind(x=1:4,y=5:8)
# Like cbind
abind(x=1:4,y=5:8,along=2)
abind(x=1:4,matrix(5:20,nrow=4),along=2)
abind(1:4,matrix(5:20,nrow=4),along=2)
# Like rbind
abind(x=1:4,matrix(5:20,nrow=4),along=1)
abind(1:4,matrix(5:20,nrow=4),along=1)
# Create a 3-d array out of two matrices
abind(x=matrix(1:16,nrow=4),y=matrix(17:32,nrow=4),along=3)
# Use of hier.names
abind(x=cbind(a=1:3,b=4:6), y=cbind(a=7:9,b=10:12), hier.names=TRUE)
# Use a list argument
abind(list(x=x, y=x), along=3)
# Use lapply(..., get) to get the objects
an <- c('x','y')
names(an) <- an
abind(lapply(an, get), along=3)
