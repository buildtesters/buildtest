library(tm)
(ptd <- PlainTextDocument("A simple plain text document",
heading = "Plain text document",
id = basename(tempfile()),
language = "en"))
meta(ptd)
