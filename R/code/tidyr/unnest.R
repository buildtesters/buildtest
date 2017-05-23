# https://cran.r-project.org/web/packages/tidyr/tidyr.pdf
library(tidyr)
library(dplyr)
df <- data_frame(
x = 1:3,
y = c("a", "d,e,f", "g,h")
)
df %>%
transform(y = strsplit(y, ",")) %>%
unnest(y)
# Or just
df %>%
unnest(y = strsplit(y, ","))
# It also works if you have a column that contains other data frames!
df <- data_frame(
x = 1:2,
y = list(
data_frame(z = 1),
data_frame(z = 3:4)
)
)
df %>% unnest(y)
# You can also unnest multiple columns simultaneously
df <- data_frame(
a = list(c("a", "b"), "c"),
b = list(1:2, 3),
c = c(11, 22)
)
df %>% unnest(a, b)
# If you omit the column names, it'll unnest all list-cols
df %>% unnest()
# Nest and unnest are inverses
df <- data.frame(x = c(1, 1, 2), y = 3:1)
df %>% nest(y)
df %>% nest(y) %>% unnest()
# If you have a named list-column, you may want to supply .id
df <- data_frame(
x = 1:2,
y = list(a = 1, b = 3:4)
)
unnest(df, .id = "name")

