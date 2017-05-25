library(TraMineR)
## Defining a sequence object with columns 10 to 25
## of a subset of the 'biofam' example data set.
data(biofam)
biofam.seq <- seqdef(biofam[501:600,10:25])
## Optimal matching using transition rates based substitution-cost matrix
## and insertion/deletion costs of 3
trcost <- seqcost(biofam.seq, method="TRATE")
biofam.om <- seqdist(biofam.seq, method="OM", indel=3, sm=trcost$sm)
## Using the insertion/deletion cost returned by seqcost
biofam.om <- seqdist(biofam.seq, method="OM", indel=trcost$indel, sm=trcost$sm)
## Using costs based on FUTURE with a forward lag of 4
fucost <- seqcost(biofam.seq, method="FUTURE", lag=4)
biofam.om <- seqdist(biofam.seq, method="OM", indel=fucost$indel, sm=fucost$sm)
## Optimal matching using a unique substitution cost of 2
## and an insertion/deletion cost of 3
ccost <- seqsubm(biofam.seq, method="CONSTANT", cval=2)
biofam.om.c2 <- seqdist(biofam.seq, method="OM",indel=3, sm=ccost)
## Displaying the distance matrix for the first 10 sequences
biofam.om.c2[1:10,1:10]
## =================================
## Example with weights and missings
## =================================
data(ex1)
ex1.seq <- seqdef(ex1,1:13, weights=ex1$weights)
## Unweighted
subm <- seqcost(ex1.seq, method="TRATE", with.missing=TRUE, weighted=FALSE)
ex1.om <- seqdist(ex1.seq, method="OM", sm=subm$sm, with.missing=TRUE)
## Weighted
subm.w <- seqcost(ex1.seq, method="TRATE", with.missing=TRUE, weighted=TRUE)
ex1.omw <- seqdist(ex1.seq, method="OM", sm=subm.w$sm, with.missing=TRUE)
ex1.om == ex1.omw

