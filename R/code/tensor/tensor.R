# https://cran.r-project.org/web/packages/tensor/tensor.pdf
library(tensor)
A <- matrix(1:6, 2, 3)
dimnames(A) <- list(happy = LETTERS[1:2], sad = NULL)
B <- matrix(1:12, 4, 3)
stopifnot(A %*% t(B) == tensor(A, B, 2, 2))
A <- A %o% A
C <- tensor(A, B, 2, 2)
stopifnot(all(dim(C) == c(2, 2, 3, 4)))
D <- tensor(C, B, c(4, 3), c(1, 2))
stopifnot(all(dim(D) == c(2, 2)))
E <- matrix(9:12, 2, 2)
s <- tensor(D, E, 1:2, 1:2)
stopifnot(s == sum(D * E), is.null(dim(s)))
