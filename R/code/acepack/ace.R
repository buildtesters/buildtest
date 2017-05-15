#! https://cran.r-project.org/web/packages/acepack/acepack.pdf
library(acepack)
TWOPI <- 8*atan(1)
x <- runif(200,0,TWOPI)
y <- exp(sin(x)+rnorm(200)/2)
a <- ace(x,y)
par(mfrow=c(3,1))
plot(a$y,a$ty) # view the response transformation
plot(a$x,a$tx) # view the carrier transformation
plot(a$tx,a$ty) # examine the linearity of the fitted model
# example when x is a matrix
X1 <- 1:10
X2 <- X1^2
X <- cbind(X1,X2)
Y <- 3*X1+X2
a1 <- ace(X,Y)
plot(rowSums(a1$tx),a1$y)
(lm(a1$y ~ a1$tx)) # shows that the colums of X are equally weighted
# From D. Wang and M. Murphy (2005), Identifying nonlinear relationships
# regression using the ACE algorithm. Journal of Applied Statistics,
# 32, 243-258.
X1 <- runif(100)*2-1
X2 <- runif(100)*2-1
X3 <- runif(100)*2-1
X4 <- runif(100)*2-1
# Original equation of Y:
Y <- log(4 + sin(3*X1) + abs(X2) + X3^2 + X4 + .1*rnorm(100))
# Transformed version so that Y, after transformation, is a
# linear function of transforms of the X variables:
# exp(Y) = 4 + sin(3*X1) + abs(X2) + X3^2 + X4
a1 <- ace(cbind(X1,X2,X3,X4),Y)
# For each variable, show its transform as a function of
# the original variable and the of the transform that created it,
# showing that the transform is recovered.
par(mfrow=c(2,1))
plot(X1,a1$tx[,1])
plot(sin(3*X1),a1$tx[,1])
plot(X2,a1$tx[,2])
plot(abs(X2),a1$tx[,2])
plot(X3,a1$tx[,3])
plot(X3^2,a1$tx[,3])
plot(X4,a1$tx[,4])
plot(X4,a1$tx[,4])
plot(Y,a1$ty)
plot(exp(Y),a1$ty)
