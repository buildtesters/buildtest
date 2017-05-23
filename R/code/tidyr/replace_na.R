# https://cran.r-project.org/web/packages/tidyr/tidyr.pdf
library(tidyr)
library(dplyr)
df <- data_frame(x = c(1, 2, NA), y = c("a", NA, "b"))
df %>% replace_na(list(x = 0, y = "unknown"))

