# https://cran.r-project.org/web/packages/flashClust/flashClust.pdf
# generate some data to cluster
library(flashClust)
set.seed(1);
nNodes = 2000;
# Random "distance" matrix
dst = matrix(runif(n = nNodes^2, min = 0, max = 1), nNodes, nNodes);
# Time the flashClust clustering
system.time( {
h1 = hclust(as.dist(dst), method= "average");
} );
# Time the standard R clustering
system.time( {
h2 = stats::hclust(as.dist(dst), method = "average");
} );
all.equal(h1, h2)
# What is different:
h1[[6]]
h2[[6]]
# Everything but the 'call' component is the same; in particular, the trees are exactly equal.
