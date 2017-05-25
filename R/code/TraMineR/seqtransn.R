library(TraMineR)
## Creating a sequence object from columns 13 to 24
## in the 'actcal' example data set
data(actcal)
actcal.seq <- seqdef(actcal,13:24)
## Computing the number of transitions
actcal.trans <- seqtransn(actcal.seq)
## Displaying the DSS for the first 10 sequences
actcal.trans[1:10]
## Example with with.missing argument
data(ex1)
ex1.seq <- seqdef(ex1, 1:13)
seqtransn(ex1.seq)
seqtransn(ex1.seq, with.missing=TRUE)
