library(TraMineR)
## Defining a state sequence object
data(mvad)
mvad.seq <- seqdef(mvad[, 17:86])
## Building dissimilarities (any dissimilarity measure can be used)
mvad.ham <- seqdist(mvad.seq, method="HAM")
## Pseudo variance of the sequences
print(dissvar(mvad.ham))
