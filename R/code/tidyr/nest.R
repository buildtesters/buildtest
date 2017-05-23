# https://cran.r-project.org/web/packages/tidyr/tidyr.pdf
library(tidyr)
library(dplyr)
iris %>% nest(-Species)
chickwts %>% nest(weight)
if (require("gapminder")) {
gapminder %>%
group_by(country, continent) %>%
nest()
gapminder %>%
nest(-country, -continent)
}
