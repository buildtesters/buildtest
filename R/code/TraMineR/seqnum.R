library(TraMineR)
data(actcal)
actcal.seq <- seqdef(actcal,13:24)
## The first 10 sequences in the actcal.seq
## sequence object
actcal.seq[1:10,]
alphabet(actcal.seq)
## The first 10 sequences in the actcal.seq
## sequence object with numerical alphabet
seqnum(actcal.seq[1:10,])
## states A,B,C,D are now coded 0,1,2,3
alphabet(seqnum(actcal.seq))
