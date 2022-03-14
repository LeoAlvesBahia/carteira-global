import string
from configparser import ConfigParser
from datetime import datetime

import psycopg2


class DbConnect:
    """Database class
    """
    def __init__(self, env: str):
        db = self.read_config(env)

        self.host = db.get('host')
        self.port = db.get('port')
        self.dbname = db.get('database')
        self.username = db.get('user')
        self.password = db.get('password')

    def read_config(self, env: str, filename: str='engine/database/database.ini') -> dict:
        parser = ConfigParser()
        print(f'Reading database configuration file: {filename}')
        parser.read(filename)

        db = {}
        if parser.has_section(env):
            params = parser.items(env)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f'Sessão {env} não encontrada no arquivo {filename}')

        return db

    def db_connect(self) -> psycopg2.extensions.connection:
        print(f'Connecting to {self.host}')
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.dbname,
            user=self.username,
            password=self.password
        )

def db_populate(data: dict, conn: psycopg2.extensions.connection) -> bool:
    rows = []
    for row in data:
        rows.append((row['CNPJ_FUNDO'].translate(str.maketrans('', '', string.punctuation)), row['VL_QUOTA'], row['DT_COMPTC']))

    with conn.cursor() as cursor:
        print('Starting query setup')
        args_str = ','.join(cursor.mogrify('(%s, %s, %s)', row).decode('UTF-8') for row in rows)
        print('Inserting into database')
        cursor.execute(f"""
            INSERT INTO fund_report (cnpj, quote_value, date_report)
            VALUES {args_str}
        """)

    return True

def db_select(conn: psycopg2.extensions.connection, init_date: datetime, end_date: datetime, cnpj: str='%%') -> list:
    with conn.cursor() as cursor:
        args_str = cursor.mogrify(
            'cnpj = %s AND date_report BETWEEN %s AND %s',
            (cnpj, init_date, end_date)
        ).decode('UTF-8')
        cursor.execute(f"""
            SELECT quote_value, date_report
            FROM fund_report
            WHERE {args_str}
        """)
        response = cursor.fetchall()
        for i, value in enumerate(response):
            response[i] = {
                'quote_value': value[0],
                'date_report': value[1].strftime('%Y-%m-%d')
            }
        return response
