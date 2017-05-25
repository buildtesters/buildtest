library(TraMineR)
data(actcal)
actcal.seq <- seqdef(actcal,13:24)
## Summarize and plots an histogram
## of the within sequence entropy
actcal.ient <- seqient(actcal.seq)
summary(actcal.ient)
hist(actcal.ient)
## Examples using with.missing argument
data(ex1)
ex1.seq <- seqdef(ex1, 1:13, weights=ex1$weights)
seqient(ex1.seq)
seqient(ex1.seq, with.missing=TRUE)
