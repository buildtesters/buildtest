library(TraMineR)
## Loading the mvad data set and creating a sequence object
data(mvad)
mvad.labels <- c("employment", "further education", "higher education",
"joblessness", "school", "training")
mvad.scodes <- c("EM","FE","HE","JL","SC","TR")
mvad.seq <- seqdef(mvad, 15:86, states=mvad.scodes, labels=mvad.labels)
## Computing the mean times
mvad.meant <- seqmeant(mvad.seq)
## Plotting
plot(mvad.meant, main="Mean durations in each state of the alphabet")
## Changing the y axis limits
plot(mvad.meant, main="Mean durations in each state of the alphabet",
ylim=c(0,40))
## Displaying error bars
mvad.meant.e <- seqmeant(mvad.seq, serr=TRUE)
plot(mvad.meant.e, main="Mean durations in each state of the alphabet",
ylim=c(0,40))

