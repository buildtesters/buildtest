library(TraMineR)
## Creating a sequence object from the actcal data set
data(actcal)
actcal.lab <- c("> 37 hours", "19-36 hours", "1-18 hours", "no work")
actcal.seq <- seqdef(actcal, 13:24, labels=actcal.lab)
## 10 most frequent sequences in the data
seqtab(actcal.seq)
## With idxs=0, we get all distinct sequences in the data set
## sorted in decreasing order of their frequency
seqtab(actcal.seq, idxs=0)
## Example with weights
## from biofam data set using weigths
data(ex1)
ex1.seq <- seqdef(ex1, 1:13, weights=ex1$weights)
## Unweighted frequencies
seqtab(ex1.seq, weighted=FALSE)
## Weighted frequencies
seqtab(ex1.seq, weighted=TRUE)
