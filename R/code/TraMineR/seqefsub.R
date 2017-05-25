library(TraMineR)
data(actcal.tse)
actcal.eseq <- seqecreate(actcal.tse)
##Searching for frequent subsequences, that is, appearing at least 20 times
fsubseq <- seqefsub(actcal.eseq, min.support=20)
##The same using a percentage
fsubseq <- seqefsub(actcal.eseq, pmin.support=0.01)
##Getting a string representation of subsequences
##Ten first subsequences
fsubseq[1:10]
##Using time constraints
##Looking for subsequence starting in summer (between june and september)
fsubseq <- seqefsub(actcal.eseq, min.support=10,
constraint=seqeconstraint(age.min=6, age.max=9))
fsubseq[1:10]
##Looking for subsequence contained in summer (between june and september)
fsubseq <- seqefsub(actcal.eseq, min.support = 10,
constraint=seqeconstraint(age.min=6, age.max=9, age.max.end=9))
fsubseq[1:10]
##Looking for subsequence enclosed in a 6 month period
## and with a maximum gap of 2 month
fsubseq <- seqefsub(actcal.eseq, min.support=10,
constraint=seqeconstraint(max.gap=2, window.size=6))
fsubseq[1:10]
