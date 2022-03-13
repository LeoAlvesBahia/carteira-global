import csv
import string
from datetime import datetime
from io import StringIO
from urllib.request import urlopen

from database.DbConnect import DbConnect


def csv_to_dict(url) -> csv.DictReader:
    print(f'Downloading file {url}')
    data = urlopen(url).read().decode('UTF-8')
    print(f'Download finished')
    data_file = StringIO(data)
    return csv.DictReader(data_file, delimiter=';')

def db_populate(data: dict, conn) -> bool:
    rows = []
    for row in data:
        rows.append((row['CNPJ_FUNDO'].translate(str.maketrans('', '', string.punctuation)), row['VL_QUOTA'], row['DT_COMPTC']))

    print('Inserting into database')
    with conn.cursor() as cursor:
        args_str = ','.join(cursor.mogrify('(%s, %s, %s)', row).decode('UTF-8') for row in rows)
        cursor.execute(f"""
            INSERT INTO fund_report (cnpj, quote_value, date_report)
            VALUES {args_str}
        """)
    
    return True

def crawler(url: str):
    db = DbConnect('dev')

    with db.db_connect() as conn:
        populate_response = db_populate(csv_to_dict(url), conn)
    return populate_response
