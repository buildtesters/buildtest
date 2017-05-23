library(tkrplot)
## Not run:
## These cannot be run by examples() but should be OK when pasted
## into an interactive R session with the tcltk package loaded
tt <- tktoplevel()
bb<-1
img <-tkrplot(tt, function() plot(1:20,(1:20)^bb))
f<-function(...) {
b <- as.numeric(tclvalue("bb"))
if (b != bb) {
bb <<- b
tkrreplot(img)
}
}
s <- tkscale(tt, command=f, from=0.05, to=2.00, variable="bb",
showvalue=FALSE, resolution=0.05, orient="horiz")
tkpack(img,s)
## End(Not run)
