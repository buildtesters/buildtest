library(timeDate)
## timeDate -
# Character Vector Strings:
dts = c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
tms = c( "23:12:55", "10:34:02", "08:30:00", "11:18:23")
dts; tms
t1 <- timeDate(dts, format = "%Y-%m-%d", FinCenter = "GMT" )
t1
stopifnot(identical(t1, timeDate(dts, FinC = "GMT"))) # auto-format
timeDate(dts, format = "%Y-%m-%d", FinCenter = "Europe/Zurich")
timeDate(paste(dts, tms), format = "%Y-%m-%d %H:%M:%S",
zone = "GMT", FinCenter = "GMT")
timeDate(paste(dts, tms),
zone = "Europe/Zurich", FinCenter = "Europe/Zurich")
timeDate(paste(dts, tms), format = "%Y-%m-%d %H:%M:%S",
zone = "GMT", FinCenter = "Europe/Zurich")
## Non Standard Format:
timeDate(paste(20:31, "03.2005", sep="."), format = "%d.%m.%Y")
## Note, ISO and American Formats are Auto-Detected:
timeDate("2004-12-31", FinCenter = "GMT")
timeDate("12/11/2004", FinCenter = "GMT")
timeDate("1/31/2004") # auto-detect American format
## From POSIX?t, and using NAs
## lsec <- as.POSIXlt(.leap.seconds) ; lsec[c(2,4:6)] <- NA
## timeDate(lsec)
## dtms <- paste(dts,tms)
## dtms[2:3] <- NA
## timeDate(dtms, FinCenter = "Europe/Zurich") # but in GMT

