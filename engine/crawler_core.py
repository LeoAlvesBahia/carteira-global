from datetime import datetime

from dateutil.relativedelta import relativedelta

import tools

start = datetime.strptime('2021-12-01', '%Y-%m-%d')
end = datetime.strptime('2021-12-31', '%Y-%m-%d')


while start <= end:
    tools.crawler(f"http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{start.strftime('%Y%m')}.csv")
    start += relativedelta(months=1)
