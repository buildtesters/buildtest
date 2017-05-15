# https://cran.r-project.org/web/packages/arm/arm.pdf
library(arm)
M1 <- polr(Sat ~ Infl + Type + Cont, weights = Freq, data = housing)
display (M1)
M2 <- bayespolr(Sat ~ Infl + Type + Cont, weights = Freq, data = housing,
prior.scale=Inf, prior.df=Inf) # Same as M1
display (M2)
M3 <- bayespolr(Sat ~ Infl + Type + Cont, weights = Freq, data = housing)
display (M3)
M4 <- bayespolr(Sat ~ Infl + Type + Cont, weights = Freq, data = housing,
prior.scale=2.5, prior.df=1) # Same as M3
display (M4)
M5 <- bayespolr(Sat ~ Infl + Type + Cont, weights = Freq, data = housing,
prior.scale=2.5, prior.df=7)
display (M5)
M6 <- bayespolr(Sat ~ Infl + Type + Cont, weights = Freq, data = housing,
prior.scale=2.5, prior.df=Inf)
display (M6)
# Assign priors
M7 <- bayespolr(Sat ~ Infl + Type + Cont, weights = Freq, data = housing,
prior.mean=rep(0,6), prior.scale=rep(2.5,6), prior.df=c(1,1,1,7,7,7))
display (M7)
#### Another example
y <- factor (rep (1:10,1:10))
x <- rnorm (length(y))
x <- x - mean(x)
M8 <- polr (y ~ x)
display (M8)
M9 <- bayespolr (y ~ x, prior.scale=Inf, prior.df=Inf, prior.counts.for.bins=0)
display (M9) # same as M1
M10 <- bayespolr (y ~ x, prior.scale=Inf, prior.df=Inf, prior.counts.for.bins=10000)
display (M10)
#### Another example
y <- factor (rep (1:3,1:3))
x <- rnorm (length(y))
x <- x - mean(x)
M11 <- polr (y ~ x)
display (M11)
M12 <- bayespolr (y ~ x, prior.scale=Inf, prior.df=Inf, prior.counts.for.bins=0)
display (M12) # same as M1
M13 <- bayespolr (y ~ x, prior.scale=Inf, prior.df=Inf, prior.counts.for.bins=1)
display (M13)
M14 <- bayespolr (y ~ x, prior.scale=Inf, prior.df=Inf, prior.counts.for.bins=10)
display (M14)

