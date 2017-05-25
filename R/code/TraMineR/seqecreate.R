library(TraMineR)
##Starting with states sequences
##Loading data
data(biofam)
## Creating state sequences
biofam.seq <- seqdef(biofam,10:25,informat='STS')
## Creating event sequences from biofam
biofam.eseq <- seqecreate(biofam.seq)
## Loading data
data(actcal.tse)
## Creating sequences
actcal.eseq <- seqecreate(id=actcal.tse$id, timestamp=actcal.tse$time,
event=actcal.tse$event)
##printing sequences
actcal.eseq[1:10]
## Using the data argument
actcal.eseq <- seqecreate(data=actcal.tse)

