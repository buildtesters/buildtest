# https://cran.r-project.org/web/packages/adephylo/adephylo.pdf

library(adephylo)
if(require(ape) & require(phylobase)){
## make a tree
x <- as(rtree(20),"phylo4")
plot(x,show.node=TRUE)
## .tipToRoot
root <- rootNode(x)
.tipToRoot(x, 1, root)
lapply(1:nTips(x), function(i) .tipToRoot(x, i, root))
}
