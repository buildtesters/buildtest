library(TraMineR)
## Loading the 'actcal' example data set
data(actcal)
## Defining a sequence object with data in columns 13 to 24
## (activity status from january to december 2000)
actcal.seq <- seqdef(actcal,13:24,informat='STS')
## Computing transition rates
seqtrate(actcal.seq)
## Computing transition rates between states "A" and "B" only
seqtrate(actcal.seq, c("A","B"))
## ====================
## Example with weights
## ====================
data(ex1)
ex1.seq <- seqdef(ex1,1:13, weights=ex1$weights)
seqtrate(ex1.seq, weighted=FALSE)
seqtrate(ex1.seq, weighted=TRUE)
