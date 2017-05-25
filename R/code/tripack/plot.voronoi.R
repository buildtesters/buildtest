library(tripack)
# plot a random mosaic
plot(voronoi.mosaic(runif(100),runif(100),duplicate="remove"))
# use isometric=TRUE and all=TRUE to see the complete mosaic
# including extreme outlier points:
plot(voronoi.mosaic(runif(100),runif(100),duplicate="remove"),
all=TRUE, isometric=TRUE)
# use a part of the quakes data set:
data(quakes)
quakes.part<-quakes[(quakes[,1]<=-17 & quakes[,1]>=-19.0 &
quakes[,2]<=182.0 & quakes[,2]>=180.0),]
quakes.vm<-voronoi.mosaic(quakes.part$lon, quakes.part$lat,
duplicate="remove")
plot(quakes.vm, isometric=TRUE)
# use the whole quakes data set
# (will not work with standard memory settings, hence commented out here)
#plot(voronoi.mosaic(quakes$lon, quakes$lat, duplicate="remove"), isometric=TRUE)
