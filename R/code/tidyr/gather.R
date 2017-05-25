# https://cran.r-project.org/web/packages/tidyr/tidyr.pdf
library(tidyr)
library(dplyr)
# From http://stackoverflow.com/questions/1181060
stocks <- data_frame(
time = as.Date('2009-01-01') + 0:9,
X = rnorm(10, 0, 1),
Y = rnorm(10, 0, 2),
Z = rnorm(10, 0, 4)
)
gather(stocks, stock, price, -time)
stocks %>% gather(stock, price, -time)
# get first observation for each Species in iris data -- base R
mini_iris <- iris[c(1, 51, 101), ]
# gather Sepal.Length, Sepal.Width, Petal.Length, Petal.Wi
gather(mini_iris, key = flower_att, value = measurement,
Sepal.Length, Sepal.Width, Petal.Length, Petal.Width)
# same result but less verbose
gather(mini_iris, key = flower_att, value = measurement, -Species)
# repeat iris example using dplyr and the pipe operator
library(dplyr)
mini_iris <-
iris %>%
group_by(Species) %>%
slice(1)
mini_iris %>% gather(key = flower_att, value = measurement, -Species)

