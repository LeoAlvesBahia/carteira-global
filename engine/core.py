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

    start_quote = response[0]['quote_value']
    print(start_quote)
    end_quote = response[-1]['quote_value']
    print(end_quote)

    factor = start_quote / end_quote

    rentab = (factor - 1) * 100

    return {
        'data': rentab
    }



if __name__ == '__main__':
    app.run()
