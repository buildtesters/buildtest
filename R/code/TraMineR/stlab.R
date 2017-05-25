library(TraMineR)
## Creating a sequence object with the columns 13 to 24
## in the 'actcal' example data set
## The color palette is automatically set
data(actcal)
actcal.seq <- seqdef(actcal,13:24)
## Retrieving the color palette
stlab(actcal.seq)
seqiplot(actcal.seq)
## Changing the state labels
stlab(actcal.seq) <- c("Full time","Part time (19-36 hours)",
"Part time (1-18 hours)", "No work")
seqiplot(actcal.seq)

