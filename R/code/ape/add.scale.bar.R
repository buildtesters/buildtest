# https://cran.r-project.org/web/packages/ape/ape.pdf
library(ape)
tr <- rtree(10)
layout(matrix(1:2, 2, 1))
plot(tr)
add.scale.bar()
plot(tr)
add.scale.bar(cex = 0.7, font = 2, col = "red")
layout(matrix(1))

