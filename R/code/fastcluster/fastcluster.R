# https://cran.r-project.org/web/packages/fastcluster/fastcluster.pdf
# Taken and modified from stats::hclust
#
# hclust(...) # new method
# hclust.vector(...) # new method
# stats::hclust(...) # old method
require(fastcluster)
require(graphics)
hc <- hclust(dist(USArrests), "ave")
plot(hc)
plot(hc, hang = -1)
## Do the same with centroid clustering and squared Euclidean distance,
## cut the tree into ten clusters and reconstruct the upper part of the
## tree from the cluster centers.
hc <- hclust.vector(USArrests, "cen")
# squared Euclidean distances
hc$height <- hc$height^2
memb <- cutree(hc, k = 10)
cent <- NULL
for(k in 1:10){
cent <- rbind(cent, colMeans(USArrests[memb == k, , drop = FALSE]))
}
hc1 <- hclust.vector(cent, method = "cen", members = table(memb))
# squared Euclidean distances
hc1$height <- hc1$height^2
opar <- par(mfrow = c(1, 2))
plot(hc, labels = FALSE, hang = -1, main = "Original Tree")
plot(hc1, labels = FALSE, hang = -1, main = "Re-start from 10 clusters")
par(opar)
