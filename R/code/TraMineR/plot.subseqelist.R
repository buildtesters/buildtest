library(TraMineR)
## loading data
data(actcal.tse)
## creating sequences
actcal.eseq <- seqecreate(actcal.tse)
## Looking for frequent subsequences
fsubseq <- seqefsub(actcal.eseq,pmin.support=0.01)
## Frequence of first ten subsequences
plot(fsubseq[1:10], cex=2)
plot(fsubseq[1:10])
