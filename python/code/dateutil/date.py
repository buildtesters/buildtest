from datetime import *; 
from dateutil.relativedelta import *
NOW = datetime.now()
TODAY = date.today()
print NOW
print TODAY

NOW=NOW+relativedelta(months=+1)
print NOW
