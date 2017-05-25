library(TraMineR)
## Loading the 'actcal' example data set
data(actcal)
## Defining a sequence object with data in columns 13 to 24
## (activity status from january to december 2000)
actcal.seq <- seqdef(actcal[,13:24], informat='STS')
## Computing the sequences turbulence
turb <- seqST(actcal.seq)
## Histogram for the turbulence
hist(turb)
## Normalized turbulence
turb.norm <- seqST(actcal.seq, norm=TRUE)
