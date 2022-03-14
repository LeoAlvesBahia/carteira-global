# carteira-global
Extrair, transformar e carregar as informações limpas de um site em uma base de dados.

## Dependencias
Este projeto possui as seguintes dependecias:

`psycopg2-binary
flask
python-dateutil`

Elas podem ser instaladas manualmente ou através do comando `pip install -r requirements.txt`.

## Banco de dados
O projeto se utiliza do arquivo `engine/database/database.ini` com os dados para conexão com o banco de dados. Para utilização do banco de dados criado por mim solicitar o arquivo por e-mail.

O banco de dados pode ser populado através do script `crawler_core.py`

## Utilização
Executar o arquivo `core.py` e fazer as requisições necessárias para o endereço `http://{host}:{porta}/funds/{cnpj}/rentability`. Este endereço aceita os seguintes parametros:

`init_date`: Deve ser uma data no formato YYYY-MM-DD. É a data inicial para a busca no banco de dados. Se nenhuma data for indicada a busca será feita a partir da data 2021-01-01. O retorno desta chamada é o rendimento da data final em relação a data final.

`end_date`: Deve ser uma data no format YYYY-MM-DD. É a data final para a busca no banco de dados. Se nenhuma data for indicada a busca será feita a partir da data 2021-12-12. O retorno desta chamada é o rendimento da data final em relação a data final.

`invest_value`: É o valor que seria investido na data inicial. O retorno desta chamada contém o rendimento da data inicial até a data final e quanto seria a cota da conta caso o valor investido fosse o informado.

`return`: Este parametro atualmente pode receber o valor `full`. O retorno rá incluir as indicações diárias de rendimento. Caso seja utilizado junto ao parametro `invest_value` estas indicações levam em consideração o valor informado.
