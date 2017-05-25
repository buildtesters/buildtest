library(TraMineR)
## Converting sequences into SPS format
data(actcal)
actcal.SPS.A <- seqformat(actcal,13:24, from="STS", to="SPS")
head(actcal.SPS.A)
## SPS (compressed) format with no prefix/suffix "/" as state/duration separator
actcal.SPS.B <- seqformat(actcal,13:24,
from="STS", to="SPS", compressed=TRUE,
SPS.out=list(xfix="", sdsep="/"))
head(actcal.SPS.B)
## Converting sequences into DSS (compressed) format
actcal.DSS <- seqformat(actcal,13:24,
from="STS", to="DSS", compressed=TRUE)
head(actcal.DSS)
## Converting from SPELL to STS format
## bfspell20 contains the first 20 biofam sequences in SPELL format
## bfpdata20 ids and year when aged 15 of the considered cases
data(bfspell) ## includes bfspell20 and bfpdata20
bf.sts <- seqformat(bfspell20, from="SPELL", to="STS", process=TRUE,
id='id', begin='begin', end='end', status='states', pdata=bfpdata20,
pvar=c('id','when15'), limit=16)
names(bf.sts) <- paste0('a',15:30)
head(bf.sts)
