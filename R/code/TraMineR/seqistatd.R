library(TraMineR)
data(actcal)
actcal.seq <- seqdef(actcal,13:24)
seqistatd(actcal.seq[1:10,])
## Example using "with.missing" argument
data(ex1)
ex1.seq <- seqdef(ex1, 1:13, weights=ex1$weights)
seqistatd(ex1.seq)
seqistatd(ex1.seq, with.missing=TRUE)
