library(TraMineR)
## Define the state sequence object
data(mvad)
mvad.seq <- seqdef(mvad[, 17:86])
## Here, we use only first 100 sequences
mvad.seq <- mvad.seq[1:100,]
## Compute dissimilarities (any dissimilarity measure can be used)
mvad.ham <- seqdist(mvad.seq, method="HAM")
## And now the multi-factor analysis
print(dissmfacw(mvad.ham ~ male + Grammar + funemp +
gcse5eq + fmpr + livboth, data=mvad[1:100,], R=10))

