library(TraMineR)
data(biofam)
biofam.seq <- seqdef(biofam,10:25)
sd <- seqstatd(biofam.seq)
## Plotting the state distribution
plot(sd, type="d")
## Plotting the entropy indexes
plot(sd, type="Ht")
## ====================
## example with weights
## ====================
data(ex1)
ex1.seq <- seqdef(ex1, 1:13, weights=ex1$weights)
## Unweighted
seqstatd(ex1.seq, weighted=FALSE)
seqstatd(ex1.seq, weighted=TRUE)

