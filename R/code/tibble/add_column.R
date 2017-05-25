# https://cran.r-project.org/web/packages/tibble/tibble.pdf
library(tibble)
# add_row ---------------------------------
df <- tibble(x = 1:3, y = 3:1)
add_column(df, z = -1:1, w = 0)
# You can't overwrite existing columns
## Not run:
add_column(df, x = 4:6)
## End(Not run)
# You can't create new observations
## Not run:
add_column(df, z = 1:5)
## End(Not run)
