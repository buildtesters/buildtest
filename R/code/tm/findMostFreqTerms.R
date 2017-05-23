library(tm)
data("crude")
## Term frequencies:
tf <- termFreq(crude[[14L]])
findMostFreqTerms(tf)
## Document-term matrices:
dtm <- DocumentTermMatrix(crude)
## Most frequent terms for each document:
findMostFreqTerms(dtm)
## Most frequent terms for the first 10 the second 10 documents,
## respectively:
findMostFreqTerms(dtm, INDEX = rep(1 : 2, each = 10L))
