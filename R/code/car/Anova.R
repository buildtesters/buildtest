# https://cran.r-project.org/web/packages/car/car.pdf
library(car)
## Two-Way Anova
mod <- lm(conformity ~ fcategory*partner.status, data=Moore,
contrasts=list(fcategory=contr.sum, partner.status=contr.sum))
Anova(mod)
## One-Way MANOVA
## See ?Pottery for a description of the data set used in this example.
summary(Anova(lm(cbind(Al, Fe, Mg, Ca, Na) ~ Site, data=Pottery)))
## MANOVA for a randomized block design (example courtesy of Michael Friendly:
## See ?Soils for description of the data set)
soils.mod <- lm(cbind(pH,N,Dens,P,Ca,Mg,K,Na,Conduc) ~ Block + Contour*Depth,
data=Soils)
Manova(soils.mod)
summary(Anova(soils.mod), univariate=TRUE, multivariate=FALSE,
p.adjust.method=TRUE)
## a multivariate linear model for repeated-measures data
## See ?OBrienKaiser for a description of the data set used in this example.
phase <- factor(rep(c("pretest", "posttest", "followup"), c(5, 5, 5)),
levels=c("pretest", "posttest", "followup"))
hour <- ordered(rep(1:5, 3))
idata <- data.frame(phase, hour)
idata
mod.ok <- lm(cbind(pre.1, pre.2, pre.3, pre.4, pre.5,
post.1, post.2, post.3, post.4, post.5,
fup.1, fup.2, fup.3, fup.4, fup.5) ~ treatment*gender,
data=OBrienKaiser)
(av.ok <- Anova(mod.ok, idata=idata, idesign=~phase*hour))
summary(av.ok, multivariate=FALSE)
## A "doubly multivariate" design with two distinct repeated-measures variables
## (example courtesy of Michael Friendly)
## See ?WeightLoss for a description of the dataset.
imatrix <- matrix(c(
1,0,-1, 1, 0, 0,
1,0, 0,-2, 0, 0,
1,0, 1, 1, 0, 0,
0,1, 0, 0,-1, 1,
0,1, 0, 0, 0,-2,
0,1, 0, 0, 1, 1), 6, 6, byrow=TRUE)
colnames(imatrix) <- c("WL", "SE", "WL.L", "WL.Q", "SE.L", "SE.Q")
rownames(imatrix) <- colnames(WeightLoss)[-1]
(imatrix <- list(measure=imatrix[,1:2], month=imatrix[,3:6]))
contrasts(WeightLoss$group) <- matrix(c(-2,1,1, 0,-1,1), ncol=2)
(wl.mod<-lm(cbind(wl1, wl2, wl3, se1, se2, se3)~group, data=WeightLoss))
Anova(wl.mod, imatrix=imatrix, test="Roy")
## mixed-effects models examples:
## Not run:
library(nlme)
example(lme)
Anova(fm2)
## End(Not run)
## Not run:
library(lme4)
example(glmer)
Anova(gm1)
## End(Not run)

