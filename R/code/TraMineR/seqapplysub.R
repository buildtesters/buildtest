library(TraMineR)
## Loading data
data(actcal.tse)
## Creating the event sequence object
actcal.eseq <- seqecreate(actcal.tse)
## Printing sequences
actcal.eseq[1:10]
## Looking for frequent subsequences
fsubseq <- seqefsub(actcal.eseq,pmin.support=0.01)
## Counting the number of occurrences of each subsequence
msubcount <- seqeapplysub(fsubseq,method="count")
## First lines...
msubcount[1:10,1:10]
## Presence-absence of each subsequence
msubpres <- seqeapplysub(fsubseq,method="presence")
## First lines...
msubpres[1:10,1:10]
## Age at first appearance of each subsequence
msubage <- seqeapplysub(fsubseq,method="age")
## First lines...
msubage[1:10,1:10]

