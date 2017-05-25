library(TraMineR)
## Defining a state sequence object
data(mvad)
mvad.seq <- seqdef(mvad[, 17:86])
## Building dissimilarities (any dissimilarity measure can be used)
mvad.ham <- seqdist(mvad.seq, method="HAM")
## R=1 implies no permutation test
da <- dissassoc(mvad.ham, group=mvad$gcse5eq, R=10)
print(da)
hist(da)

