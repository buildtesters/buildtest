library(ade4)
data(acacia)
if(adegraphicsLoaded()) {
gg <- s1d.barchart(acacia, p1d.horizontal = FALSE, psub.position = "topleft",
plabels.cex = 0, ylim = c(0,20))
} else {
par(mfcol = c(5, 3))
par(mar = c(2, 2, 2, 2))
for(k in 1:15) {
barplot(acacia[, k], ylim = c(0, 20), col = grey(0.8))
ade4:::scatterutil.sub(names(acacia)[k], 1.5, "topleft")
}
par(mfcol = c(1, 1))
}
