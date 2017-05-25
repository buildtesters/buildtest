library(TraMineR)
## Loading the mvad data set and creating a sequence object
data(mvad)
mvad.labels <- c("employment", "further education", "higher education",
"joblessness", "school", "training")
mvad.scodes <- c("EM","FE","HE","JL","SC","TR")
## First 36 months trajectories
mvad.seq <- seqdef(mvad, 15:50, states=mvad.scodes, labels=mvad.labels)
## Computing Hamming distances
##
dist.ham <- seqdist(mvad.seq, method="HAM")
## Extracting a representative set using the sequence frequency
## as a representativeness criterion
mvad.rep <- seqrep(mvad.seq, diss=dist.ham)
## Plotting the representative set
plot(mvad.rep)

