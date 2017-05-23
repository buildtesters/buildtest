# https://cran.r-project.org/web/packages/tibble/tibble.pdf
library(tibble)
# add_row ---------------------------------
df <- tibble(x = 1:3, y = 3:1)
add_row(df, x = 4, y = 0)
# You can specify where to add the new rows
add_row(df, x = 4, y = 0, .before = 2)
# You can supply vectors, to add multiple rows (this isn't
# recommended because it's a bit hard to read)
add_row(df, x = 4:5, y = 0:-1)
# Absent variables get missing values
add_row(df, x = 4)
# You can't create new variables
## Not run:
add_row(df, z = 10)
## End(Not run)
