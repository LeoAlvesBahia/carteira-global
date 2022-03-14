from datetime import datetime
from pickletools import float8
from tracemalloc import start

from flask import Flask, request

import tools
from database.DbConnect import DbConnect, db_select

app = Flask(__name__)


@app.route('/funds/<cnpj>/rentability')
def rentability(cnpj: str) -> dict:
    if not tools.check_cnpj(cnpj):
        return 'CNPJ informado é inválido.', 500

    args = request.args.to_dict()

    try:
        init_date = datetime.strptime(args.get('init_date', '2021-01-01'), '%Y-%m-%d')
        end_date = datetime.strptime(args.get('end_date', '2021-12-31'), '%Y-%m-%d')
    except ValueError:
        return 'Incorrect date format. Date should be YYYY-MM-DD', 500

    db = DbConnect('dev')
    with db.db_connect() as conn:
        response = db_select(
            conn=conn,
            init_date=init_date,
            end_date=end_date,
            cnpj=cnpj
        )
    if not response:
        return 'Range of date not found in database', 500

    if 'full' == args.get('return', 'init_final'):
        return tools.full_return(response, args.get('invest_value', None))

    rentab = tools.get_rentability(response)
    if 'invest_value' in args.keys():
        return {
            'rentability': rentab,
            'equity_value': (rentab + 1) * float(args['invest_value'])
        }
    return {
        'rentability': rentab
    }

if __name__ == '__main__':
    app.run()
