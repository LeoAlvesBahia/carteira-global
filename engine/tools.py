import csv
from itertools import cycle
from io import StringIO
from urllib.request import urlopen

from database.DbConnect import DbConnect, db_populate


def csv_to_dict(url: str) -> csv.DictReader:
    print(f'Downloading file {url}')
    data = urlopen(url).read().decode('UTF-8')
    print(f'Download finished')
    data_file = StringIO(data)
    return csv.DictReader(data_file, delimiter=';')

def crawler(url: str) -> bool:
    data = csv_to_dict(url)

    db = DbConnect('dev')
    with db.db_connect() as conn:
        populate_response = db_populate(data, conn)
    return populate_response

# https://programandoautomacao.blogspot.com/2020/10/python-uma-funcao-pythonica-para_15.html
def check_cnpj(cnpj: str) -> bool:
    LENGTH_CNPJ = 14

    if len(cnpj) != LENGTH_CNPJ:
        return False

    if cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
        return False

    cnpj_r = cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            return False

    return True

def get_rentability(data: list) -> float:
    start_quote = data[0]['quote_value']
    end_quote = data[-1]['quote_value']

    factor = end_quote / start_quote

    return factor - 1

def full_return(response: list, invest_value: str=None) -> dict:
    data = [{
        'date_report': response[0]['date_report'],
        'rentability': 0,
        'equity_value': float(invest_value) if invest_value else response[0]['quote_value']
    }]
    for i in range(1, len(response)):
        rentab = get_rentability([response[i-1], response[i]])
        data.append({
            'date_report': response[i]['date_report'],
            'rentability': rentab * 100,
            'equity_value': (rentab + 1) * data[-1]['equity_value']
        })
    return {
        'data': data
    }
