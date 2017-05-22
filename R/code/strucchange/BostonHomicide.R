# https://cran.r-project.org/web/packages/strucchange/strucchange.pdf
library(strucchange)
data("BostonHomicide")
attach(BostonHomicide)
## data from Table 1
tapply(homicides, year, mean)
populationBM[0:6*12 + 7]
tapply(ahomicides25, year, mean)
tapply(ahomicides35, year, mean)
population[0:6*12 + 7]
unemploy[0:6*12 + 7]
## model A
## via OLS
fmA <- lm(homicides ~ populationBM + season)
anova(fmA)
## as GLM
fmA1 <- glm(homicides ~ populationBM + season, family = poisson)
anova(fmA1, test = "Chisq")
## model B & C
fmB <- lm(homicides ~ populationBM + season + ahomicides25)
fmC <- lm(homicides ~ populationBM + season + ahomicides25 + unemploy)
detach(BostonHomicide)
