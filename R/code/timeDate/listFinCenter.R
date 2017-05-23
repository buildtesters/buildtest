library(timeDate)
## myFinCenter - the global setting currently used:
getRmetricsOptions("myFinCenter")
## Other Financial Centers:
listFinCenter("Asia/")
listFinCenter("^A") # all beginning with "A"
listFinCenter("^[^A]") # all *not* beginning with "A"
listFinCenter(".*/L") # cities with L*
stopifnot(identical(sort(listFinCenter()), ## 'A' and 'not A' == everything:
sort(union(listFinCenter("^A"),
listFinCenter("^[^A]")))))
