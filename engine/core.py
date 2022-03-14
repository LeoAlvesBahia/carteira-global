from datetime import datetime
from tracemalloc import start

from flask import Flask, request

import tools
from database.DbConnect import DbConnect, db_select

app = Flask(__name__)


@app.route('/funds/<cnpj>/rentability')
def rentability(cnpj):
    if not tools.check_cnpj(cnpj):
        return 'CNPJ informado é inválido.', 500

    args = request.args.to_dict()

    try:
        init_date = datetime.strptime(args.get('init_date', '2021-01-01'), '%Y-%m-%d')
        end_date = datetime.strptime(args.get('end_date', '2021-12-31'), '%Y-%m-%d')
    except ValueError:
        raise ValueError('Incorrect date format. Date should be YYYY-MM-DD')

    db = DbConnect('dev')
    with db.db_connect() as conn:
        response = db_select(
            conn=conn,
            init_date=init_date,
            end_date=end_date,
            cnpj=cnpj
        )

    rentab = tools.get_rentability(tools.get_factor(response))

    if 'invest_value' in args.keys():
        return {
            'rentability': rentab,
            'equity_value': args['invest_value'] * rentab
        }

    return {
        'rentability': rentab
    }

@app.route('/funds/<cnpj>/rentability')
def invest_value(cnpj):
    if not tools.check_cnpj(cnpj):
        return 'CNPJ informado é inválido.', 500

    args = request.args.to_dict()
    if 'init_date' not in args.keys():
        raise TypeError('init_date parameter missing')
    if 'end_date' not in args.keys():
        raise TypeError('end_date parameter missing')

if __name__ == '__main__':
    app.run()
