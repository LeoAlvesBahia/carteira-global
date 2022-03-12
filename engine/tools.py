import csv
from io import StringIO
from urllib.request import urlopen


def crawler(url):
    data = urlopen(url).read().decode('UTF-8')
    data_file = StringIO(data)
    csv_reader = csv.DictReader(data_file, delimiter=';')

    count = 0
    for row in csv_reader:
        print(row)
        count += 1
        if count == 3:
            break


crawler('http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_202101.csv')
