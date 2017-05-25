# https://cran.r-project.org/web/packages/beanplot/beanplot.pdf
library(beanplot)
beanplot(rnorm(22),rnorm(22),rnorm(22),main="Test!",rnorm(3))
#mostly examples taken from boxplot:
par(mfrow = c(1,2))
boxplot(count ~ spray, data = InsectSprays, col = "lightgray")
beanplot(count ~ spray, data = InsectSprays, col = "lightgray", border = "grey", cutmin = 0)
boxplot(count ~ spray, data = InsectSprays, col = "lightgray")
beanplot(count ~ spray, data = InsectSprays, col = "lightgray", border = "grey",
overallline = "median")
boxplot(decrease ~ treatment, data = OrchardSprays,
log = "y", col = "bisque", ylim = c(1,200))
beanplot(decrease ~ treatment, data = OrchardSprays,
col = "bisque", ylim = c(1,200))
par(mfrow = c(2,1))
mat <- cbind(Uni05 = (1:100)/21, Norm = rnorm(100),
T5 = rt(100, df = 5), Gam2 = rgamma(100, shape = 2))
par(las=1)# all axis labels horizontal
boxplot(data.frame(mat), main = "boxplot(*, horizontal = TRUE)",
horizontal = TRUE, ylim = c(-5,8))
beanplot(data.frame(mat), main = "beanplot(*, horizontal = TRUE)",
horizontal = TRUE, ylim = c(-5,8))
par(mfrow = c(1,2))
boxplot(len ~ dose, data = ToothGrowth,
boxwex = 0.25, at = 1:3 - 0.2,
subset = supp == "VC", col = "yellow",
main = "Guinea Pigs' Tooth Growth",
xlab = "Vitamin C dose mg",
ylab = "tooth length", ylim = c(-1, 40), yaxs = "i")
boxplot(len ~ dose, data = ToothGrowth, add = TRUE,
boxwex = 0.25, at = 1:3 + 0.2,
subset = supp == "OJ", col = "orange")
legend("bottomright", bty="n", c("Ascorbic acid", "Orange juice"),
fill = c("yellow", "orange"))
allplot <- beanplot(len ~ dose+supp, data = ToothGrowth,
what=c(TRUE,FALSE,FALSE,FALSE),show.names=FALSE,ylim=c(-1,40), yaxs = "i")
beanplot(len ~ dose, data = ToothGrowth, add=TRUE,
boxwex = 0.6, at = 1:3*2 - 0.9,
subset = supp == "VC", col = "yellow",border="yellow2",
main = "Guinea Pigs' Tooth Growth",
xlab = "Vitamin C dose mg",
ylab = "tooth length", ylim = c(3, 40), yaxs = "i",
bw = allplot$bw, wd = allplot$wd, what = c(FALSE,TRUE,TRUE,TRUE))
beanplot(len ~ dose, data = ToothGrowth, add = TRUE,
boxwex = 0.6, at = 1:3*2-0.1,
subset = supp == "OJ", col = "orange",border="darkorange",
bw = allplot$bw, wd = allplot$wd, what = c(FALSE,TRUE,TRUE,TRUE))
legend("bottomright", bty="n", c("Ascorbic acid", "Orange juice"),
fill = c("yellow", "orange"))
par(mfrow = c(1,2))
boxplot(len ~ dose, data = ToothGrowth,
boxwex = 0.25, at = 1:3 - 0.2,
subset = supp == "VC", col = "yellow",
main = "Guinea Pigs' Tooth Growth",
xlab = "Vitamin C dose mg",
ylab = "tooth length", ylim = c(-1, 40), yaxs = "i")
boxplot(len ~ dose, data = ToothGrowth, add = TRUE,
boxwex = 0.25, at = 1:3 + 0.2,
subset = supp == "OJ", col = "orange")
legend("bottomright", bty="n",c("Ascorbic acid", "Orange juice"),
fill = c("yellow", "orange"))
beanplot(len ~ reorder(supp, len, mean) * dose, ToothGrowth,
side = "b", col = list("yellow", "orange"), border = c("yellow2",
"darkorange"), main = "Guinea Pigs' Tooth Growth",
xlab = "Vitamin C dose mg", ylab = "tooth length", ylim = c(-1,
40), yaxs = "i")
legend("bottomright", bty="n",c("Ascorbic acid", "Orange juice"),
fill = c("yellow", "orange"))
#Example with multiple vectors and/or formulas
par(mfrow = c(2,1))
beanplot(list(all = ToothGrowth$len), len ~ supp, ToothGrowth, len ~ dose)
title("Tooth growth length (beanplot)")
#Trick using internal functions to do this with other functions:
mboxplot <- function(...){
graphics::boxplot(beanplot:::getgroupsfromarguments(), ...)
}
mstripchart <- function(..., method = "overplot", jitter = 0.1, offset = 1/3,
vertical = TRUE, group.names, add = FALSE,
at = NULL, xlim = NULL, ylim = NULL,
ylab = NULL, xlab=NULL, dlab = "", glab = "",
log = "", pch = 0, col = par("fg"), cex = par("cex"),
axes = TRUE, frame.plot = axes) {
graphics::stripchart(beanplot:::getgroupsfromarguments(),
method, jitter, offset, vertical, group.names, add,
at, xlim, ylim, ylab, xlab, dlab, glab, log, pch, col, cex,
axes, frame.plot)
}
mstripchart(list(all = ToothGrowth$len), len ~ supp, ToothGrowth, len ~ dose,
xlim = c(0.5,6.5))
title("Tooth growth length (stripchart)")
