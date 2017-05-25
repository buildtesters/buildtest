library(TraMineR)
## Creating a state sequence object from columns 13 to 24
## in the 'actcal' example data set
data(actcal)
actcal.seq <- seqdef(actcal,13:24,
labels=c("FullTime", "PartTime", "LowPartTime", "NoWork"))
## Creating a transition matrix, one event per transition
seqetm(actcal.seq,method = "transition")
## Creating a transition matrix, single to-state events
seqetm(actcal.seq,method = "state")
## Creating a transition matrix, two events per transition
seqetm(actcal.seq,method = "period")
## changing the prefix of period start event.
seqetm(actcal.seq,method = "period", bp="begin")
