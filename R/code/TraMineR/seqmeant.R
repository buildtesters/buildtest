library(TraMineR)
## Defining a sequence object with columns 13 to 24
## in the actcal example data set
data(actcal)
actcal.lab <- c("> 37 hours", "19-36 hours", "1-18 hours", "no work")
actcal.seq <- seqdef(actcal,13:24,labels=actcal.lab)
## Computing the mean time in the different states
seqmeant(actcal.seq)
## Mean times with their standard error
seqmeant(actcal.seq, serr=TRUE)
