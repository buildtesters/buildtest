# https://cran.r-project.org/web/packages/tensorA/tensorA.pdf
library(tensorA)
A <- to.tensor(1:20,c(U=2,V=2,W=5))
add.tensor(A,A)/2 -A
(A+A)/2
A/A
A * 1/A
norm.tensor(reorder.tensor(A,c(2,3,1)) - A)
