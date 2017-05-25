library(TraMineR)
## Creating a sequence object from the actcal data set
data(actcal)
actcal.lab <- c("> 37 hours", "19-36 hours", "1-18 hours", "no work")
actcal.seq <- seqdef(actcal, 13:24, labels=actcal.lab)
## States frequencies
seqstatf(actcal.seq)
## Example with weights
data(ex1)
ex1.seq <- seqdef(ex1, 1:13, weights=ex1$weights)
## Unweighted
seqstatf(ex1.seq, weighted=FALSE)
## Weighted
seqstatf(ex1.seq, weighted=TRUE)
