# https://cran.r-project.org/web/packages/TH.data/TH.data.pdf
library(TH.data)
data("bodyfat", package = "TH.data")
### final model proposed by Garcia et al. (2005)
fmod <- lm(DEXfat ~ hipcirc + anthro3a + kneebreadth, data = bodyfat)
coef(fmod)

