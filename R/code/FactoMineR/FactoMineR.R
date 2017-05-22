# https://cran.r-project.org/web/packages/FactoMineR/FactoMineR.pdf
## Example two-way anova
library(FactoMineR)
data(senso)
res <- AovSum(Score~ Product + Day , data=senso)
res
## Example two-way anova with interaction
data(senso)
res2 <- AovSum(Score~ Product + Day + Product : Day, data=senso)
res2
## Example ancova
data(footsize)
res3 <- AovSum(footsize ~ size + sex + size : sex, data=footsize)
res3

