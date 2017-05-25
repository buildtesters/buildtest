library(TraMineR)
## Creating a sequence object with the columns 13 to 24
## in the 'actcal' example data set
data(actcal)
actcal.seq <- seqdef(actcal,13:24,
labels=c("> 37 hours", "19-36 hours", "1-18 hours", "no work"))
## Displaying the first 10 rows of the sequence object
actcal.seq[1:10,]
## Displaying the first 10 rows of the sequence object
## in SPS format
print(actcal.seq[1:10,], format="SPS")
## Plotting the first 10 sequences
plot(actcal.seq)
## Re-ordering the alphabet
actcal.seq <- seqdef(actcal,13:24,alphabet=c("B","A","D","C"))
alphabet(actcal.seq)
## Adding a state not appearing in the data to the
## alphabet
actcal.seq <- seqdef(actcal,13:24,alphabet=c("A","B","C","D","E"))
alphabet(actcal.seq)
## Adding a state not appearing in the data to the
## alphabet and changing the states labels
actcal.seq <- seqdef(actcal,13:24,
alphabet=c("A","B","C","D","E"),
states=c("FT","PT","LT","NO","TR"))
alphabet(actcal.seq)
actcal.seq[1:10,]
## ============================
## Example with missing values
## ============================
data(ex1)
## With right="DEL" default value
seqdef(ex1,1:13)
## Eliminating 'left' missing values
seqdef(ex1,1:13, left="DEL")
## Eliminating 'left' missing values and gaps
seqdef(ex1,1:13, left="DEL", gaps="DEL")
## ====================
## Example with weights
## ====================
ex1.seq <- seqdef(ex1, 1:13, weights=ex1$weights)
## weighted sequence frequencies
seqtab(ex1.seq)

