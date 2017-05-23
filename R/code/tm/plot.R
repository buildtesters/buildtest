library(tm)
## Not run: data(crude)
tdm <- TermDocumentMatrix(crude,
control = list(removePunctuation = TRUE,
removeNumbers = TRUE,
stopwords = TRUE))
plot(tdm, corThreshold = 0.2, weighting = TRUE)
## End(Not run)
