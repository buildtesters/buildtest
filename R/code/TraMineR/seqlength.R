library(TraMineR)
## Loading the 'famform' example data set
data(famform)
## Defining a sequence object with the 'famform' data set
ff.seq <- seqdef(famform)
## Retrieving the length of the first 10 sequences
## in the ff.seq sequence object
seqlength(ff.seq)
