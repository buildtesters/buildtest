# https://cran.r-project.org/web/packages/tidyr/tidyr.pdf
library(tidyr)
library(dplyr, warn.conflicts = FALSE)
df <- data_frame(
group = c(1:2, 1),
item_id = c(1:2, 2),
item_name = c("a", "b", "b"),
value1 = 1:3,
value2 = 4:6
)
df %>% complete(group, nesting(item_id, item_name))
# You can also choose to fill in missing values
df %>% complete(group, nesting(item_id, item_name), fill = list(value1 = 0))
