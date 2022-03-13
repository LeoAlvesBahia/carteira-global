from flask import Flask, request

from database.DbConnect import DbConnect

import tools

app = Flask(__name__)


@app.route('/funds/<cnpj>/rentability')
def rentability(cnpj):
    if not tools.check_cnpj(cnpj):
        return 'CNPJ informado é inválido.', 500

    args = request.args.to_dict()

    
    print(args)
    return cnpj



if __name__ == '__main__':
    app.run()
