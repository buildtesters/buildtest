# https://cran.r-project.org/web/packages/bio3d/bio3d.pdf
library(bio3d)
## Load AAindex data
data(aa.index)
## Find all indeces described as "volume"
ind <- which(sapply(aa.index, function(x)
length(grep("volume", x$D, ignore.case=TRUE)) != 0))
## find all indeces with author "Kyte"
ind <- which(sapply(aa.index, function(x) length(grep("Kyte", x$A)) != 0))
## examine the index
aa.index[[ind]]$I
## find indeces which correlate with it
all.ind <- names(which(Mod(aa.index[[ind]]$C) >= 0.88))
## examine them all
sapply(all.ind, function (x) aa.index[[x]]$I)
