library(TraMineR)
data(biofam)
biofam.seq <- seqdef(biofam,10:25)
## Searching for the first occurrence of state 1
## in the biofam data set.
seqfpos(biofam.seq,"1")

