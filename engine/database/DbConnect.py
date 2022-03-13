import string
from configparser import ConfigParser

import psycopg2


class DbConnect:
    """Database class
    """
    def __init__(self, env):
        db = self.read_config(env)

        self.host = db.get('host')
        self.port = db.get('port')
        self.dbname = db.get('database')
        self.username = db.get('user')
        self.password = db.get('password')

    def read_config(self, env: str, filename='engine/database/database.ini') -> dict:
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

    def db_connect(self):
        print(f'Connecting to {self.host}')
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.dbname,
            user=self.username,
            password=self.password
        )

    def db_populate(self, data: dict, conn) -> bool:
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

    def db_select(self, conn, args={}):
        with conn.cursor() as cursor:
            args_str = cursor.mogrify('CNPJ = %s')
            cursor.execute(f"""
                SELECT quote_value, date_report
                FROM fund_report
                WHERE {}
            """)
