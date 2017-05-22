# https://www.rdocumentation.org/packages/tcltk/versions/3.4.0/topics/TclInterface
library(tcltk)
tclVersion()

## Not run: ------------------------------------
# ## These cannot be run by example() but should be OK when pasted
# ## into an interactive R session with the tcltk package loaded
# .Tcl("format \"%s\n\" \"Hello, World!\"")
# f <- function()cat("HI!\n")
# .Tcl.callback(f)
# .Tcl.args(text = "Push!", command = f) # NB: Different address
# 
# xyzzy <- tclVar(7913)
# tclvalue(xyzzy)
# tclvalue(xyzzy) <- "foo"
# as.character(xyzzy)
# tcl("set", as.character(xyzzy))
# 
# top <- tktoplevel() # a Tk widget, see Tk-widgets
# ls(envir = top$env, all = TRUE)
# ls(envir = .TkRoot$env, all = TRUE) # .Tcl.args put a callback ref in here
## ---------------------------------------------
