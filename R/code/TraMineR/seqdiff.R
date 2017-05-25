library(TraMineR)
## Define a state sequence object
data(mvad)
## First 12 months of the trajectories
mvad.seq <- seqdef(mvad[, 17:28])
## Position-wise discrepancy analysis
mvad.diff <- seqdiff(mvad.seq, group=mvad$gcse5eq)
print(mvad.diff)
plot(mvad.diff, stat=c("Pseudo R2", "Levene"), xtstep=6)
plot(mvad.diff, stat="discrepancy")
