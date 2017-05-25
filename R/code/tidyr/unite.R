# https://cran.r-project.org/web/packages/tidyr/tidyr.pdf
library(tidyr)
library(dplyr)
unite_(mtcars, "vs_am", c("vs","am"))
# Separate is the complement of unite
mtcars %>%
unite(vs_am, vs, am) %>%
separate(vs_am, c("vs", "am"))

