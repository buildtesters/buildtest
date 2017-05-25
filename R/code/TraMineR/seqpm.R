library(TraMineR)
data(actcal)
actcal.seq <- seqdef(actcal,13:24)
## search for pattern "DAAD"
## (no work-full time work-full time work-no work)
## results are stored in the 'daad' object
daad <- seqpm(actcal.seq,"DAAD")
## Looking at the sequences
## containing the pattern
actcal.seq[daad$MIndex,]
## search for pattern "AD"
## (full time work-no work)
seqpm(actcal.seq,"AD")
