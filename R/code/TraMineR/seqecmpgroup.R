library(TraMineR)
data(actcal.tse)
actcal.eseq <- seqecreate(actcal.tse)
##Searching for frequent subsequences, that is, appearing at least 20 times
fsubseq <- seqefsub(actcal.eseq, pmin.support=0.01)
##searching for susbsequences discriminating the most men and women
data(actcal)
discr <- seqecmpgroup(fsubseq, group=actcal$sex, method="bonferroni")
##Printing discriminating subsequences
print(discr)
##Plotting the six most discriminating subsequences
plot(discr[1:6])

