library(tm)
txt <- system.file("texts", "txt", package = "tm")
## Not run: PCorpus(DirSource(txt),
dbControl = list(dbName = "pcorpus.db", dbType = "DB1"))
## End(Not run)
