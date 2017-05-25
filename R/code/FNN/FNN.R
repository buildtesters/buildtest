# https://cran.r-project.org/web/packages/FNN/FNN.pdf
library(FNN)
data<- query<- cbind(1:10, 1:10)
get.knn(data, k=5)
get.knnx(data, query, k=5)
get.knnx(data, query, k=5, algo="kd_tree")

