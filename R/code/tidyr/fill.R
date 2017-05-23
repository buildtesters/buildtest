# https://cran.r-project.org/web/packages/tidyr/tidyr.pdf
library(tidyr)
df <- data.frame(Month = 1:12, Year = c(2000, rep(NA, 11)))
df %>% fill(Year)

