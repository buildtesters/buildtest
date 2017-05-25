library(tripack)
# example from TRIPACK:
data(tritest)
tr<-tri.mesh(tritest$x,tritest$y)
in.convex.hull(tr,0.5,0.5)
in.convex.hull(tr,c(0.5,-1,1),c(0.5,1,1))
# use a part of the quakes data set:
data(quakes)
quakes.part<-quakes[(quakes[,1]<=-10.78 & quakes[,1]>=-19.4 &
quakes[,2]<=182.29 & quakes[,2]>=165.77),]
q.tri<-tri.mesh(quakes.part$lon, quakes.part$lat, duplicate="remove")
in.convex.hull(q.tri,quakes$lon[990:1000],quakes$lat[990:1000])
