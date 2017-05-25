# https://cran.r-project.org/web/packages/subplex/subplex.pdf
library(subplex)
rosen <- function (x) { ## Rosenbrock Banana function
x1 <- x[1]
x2 <- x[2]
100*(x2-x1*x1)^2+(1-x1)^2
}
subplex(par=c(11,-33),fn=rosen)
rosen2 <- function (x) {
X <- matrix(x,ncol=2)
sum(apply(X,1,rosen))
}
subplex(par=c(-33,11,14,9,0,12),fn=rosen2,control=list(maxit=30000))
ripple <- function (x) {
r <- sqrt(sum(x^2))
1-exp(-r^2)*cos(10*r)^2
}
subplex(par=c(1),fn=ripple,hessian=TRUE)
subplex(par=c(0.1,3),fn=ripple,hessian=TRUE)
subplex(par=c(0.1,3,2),fn=ripple,hessian=TRUE)
rosen <- function (x, g = 0, h = 0) { ## Rosenbrock Banana function (using names)
x1 <- x['a']
x2 <- x['b']-h
100*(x2-x1*x1)^2+(1-x1)^2+g
}
subplex(par=c(b=11,a=-33),fn=rosen,h=22,control=list(abstol=1e-9,parscale=5),hessian=TRUE)
