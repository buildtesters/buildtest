library(TraMineR)
## Loading the 'actcal' example data set
data(actcal)
## Defining a sequence object with data in columns 13 to 24
## (activity status from january to december 2000)
actcal.lab <- c("> 37 hours", "19-36 hours", "1-18 hours", "no work")
actcal.seq <- seqdef(actcal, 13:24, labels=actcal.lab)
## 10 most frequent sequences in the data
actcal.freq <- seqtab(actcal.seq)
## Plotting the object
plot(actcal.freq, main="Sequence frequencies - actcal data set")
## Plotting all the distinct sequences without borders
## and space between sequences
actcal.freq2 <- seqtab(actcal.seq, idxs=0)
plot(actcal.freq2, main="Sequence frequencies - actcal data set",
border=NA, space=0)
