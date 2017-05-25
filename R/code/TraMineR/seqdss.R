library(TraMineR)
## Creating a sequence object with the columns 13 to 24
## in the 'actcal' example data set
data(actcal)
actcal.seq <- seqdef(actcal,13:24)
## Retrieving the DSS
actcal.dss <- seqdss(actcal.seq)
## Displaying the DSS for the first 10 sequences
actcal.dss[1:10,]
## Example with with.missing argument
data(ex1)
ex1.seq <- seqdef(ex1, 1:13)
seqdss(ex1.seq)
seqdss(ex1.seq, with.missing=TRUE)

