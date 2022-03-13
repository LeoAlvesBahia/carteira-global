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
