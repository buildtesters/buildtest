library(tm)
f <- system.file("texts", "rcv1_2330.xml", package = "tm")
rcv1 <- readRCV1(elem = list(content = readLines(f)),
language = "en", id = "id1")
meta(rcv1)
