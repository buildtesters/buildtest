library(TraMineR)
data(actcal)
actcal.seq <- seqdef(actcal,13:24)
## Number of subsequences with DSS=TRUE
seqsubsn(actcal.seq[1:10,])
## Number of subsequences with DSS=FALSE
seqsubsn(actcal.seq[1:10,],DSS=FALSE)

