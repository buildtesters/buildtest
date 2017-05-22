# https://cran.r-project.org/web/packages/stringr/stringr.pdf
library(stringr)
dog <- "The quick brown dog"
str_to_upper(dog)
str_to_lower(dog)
str_to_title(dog)
# Locale matters!
str_to_upper("i") # English
str_to_upper("i", "tr") # Turkish

