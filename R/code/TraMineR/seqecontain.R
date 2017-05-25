library(TraMineR)
data(actcal.tse)
actcal.eseq <- seqecreate(actcal.tse)
##Searching for frequent subsequences, that is appearing at least 20 times
fsubseq <- seqefsub(actcal.eseq,min.support=20)
##looking for subsequence with FullTime
seqecontain(fsubseq,c("FullTime"))
