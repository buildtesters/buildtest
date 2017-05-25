# https://cran.r-project.org/web/packages/futile.logger/futile.logger.pdf
library(futile.logger)
flog.debug("This %s print", "won't")
flog.warn("This %s print", "will")
flog.info("This inherits from the ROOT logger", name='logger.a')
flog.threshold(DEBUG, name='logger.a')
flog.debug("logger.a has now been set to DEBUG", name='logger.a')
flog.debug("But the ROOT logger is still at INFO (so this won't print)")
## Not run:
flog.appender(appender.file("other.log"), name='logger.b')
flog.info("This writes to a %s", "file", name='logger.b')
## End(Not run)

