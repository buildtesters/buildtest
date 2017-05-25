#https://cran.r-project.org/web/packages/filehash/filehash.pdf
library(filehash)
dbCreate("myDB") ## Create database 'myDB'
db <- dbInit("myDB")
dbInsert(db, "a", 1:10)
dbInsert(db, "b", rnorm(1000))
dbExists(db, "b") ## 'TRUE'
dbList(db) ## c("a", "b")
dbDelete(db, "a")
dbList(db) ## "b"
with(db, mean(b))

