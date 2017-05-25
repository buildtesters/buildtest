# https://cran.r-project.org/web/packages/flexclust/flexclust.pdf
library(flexclust)
cl <- cclust(iris[,-5], k=3)
barplot(cl)
barplot(cl, bycluster=FALSE)
## plot the maximum instead of mean value per cluster:
barplot(cl, bycluster=FALSE, data=iris[,-5],
FUN=function(x) apply(x,2,max))
## use lattice for plotting:
barchart(cl)
## automatic abbreviation of labels
barchart(cl, scales=list(abbreviate=TRUE))
## origin of bars at zero
barchart(cl, scales=list(abbreviate=TRUE), origin=0)
## Use manual labels. Note that the flexclust barchart orders bars
## from top to bottom (the default does it the other way round), hence
## we have to rev() the labels:
LAB <- c("SL", "SW", "PL", "PW")
barchart(cl, scales=list(y=list(labels=rev(LAB))), origin=0)
## deviation of each cluster center from the population means
barchart(cl, origin=rev(cl@xcent), mlcol=NULL)
## use shading to highlight large deviations from population mean
barchart(cl, shade=TRUE)
## use smaller deviation limit than default and add a legend
barchart(cl, shade=TRUE, diff=0.2, legend=TRUE)

