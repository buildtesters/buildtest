# https://cran.r-project.org/web/packages/stringi/stringi.pdf
library(stringi)
# in Polish ch < h:
stri_cmp_lt("hladny", "chladny", locale="pl_PL")
# in Slovak ch > h:
stri_cmp_lt("hladny", "chladny", locale="sk_SK")
# < or > (depends on locale):
stri_cmp("hladny", "chladny")
# ignore case differences:
stri_cmp_equiv("hladny", "HLADNY", strength=2)
# also ignore diacritical differences:
stri_cmp_equiv("hladn\u00FD", "hladny", strength=1, locale="sk_SK")
# non-Unicode-normalized vs normalized string:
stri_cmp_equiv(stri_trans_nfkd("\u0105"), "\u105")
# note the difference:
stri_cmp_eq(stri_trans_nfkd("\u0105"), "\u105")
# ligatures:
stri_cmp_equiv("\ufb00", "ff", strength=2)
# phonebook collation
stri_cmp_equiv("G\u00e4rtner", "Gaertner", locale="de_DE@collation=phonebook", strength=1L)
stri_cmp_equiv("G\u00e4rtner", "Gaertner", locale="de_DE", strength=1L)
