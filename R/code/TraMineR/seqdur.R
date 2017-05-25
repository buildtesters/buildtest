library(TraMineR)
## Creating a sequence object with the columns 13 to 24
## in the 'actcal' example data set
data(actcal)
actcal.seq <- seqdef(actcal,13:24)
## Retrieving the DSS
actcal.dur <- seqdur(actcal.seq)
## Displaying the durations for the first 10 sequences
actcal.dur[1:10,]

