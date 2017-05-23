# https://cran.r-project.org/web/packages/tidyr/tidyr.pdf
library(tidyr)
df <- data.frame(
x = 1:3,
y = c("a", "d,e,f", "g,h"),
z = c("1", "2,3,4", "5,6"),
stringsAsFactors = FALSE
)
separate_rows(df, y, z, convert = TRUE)
