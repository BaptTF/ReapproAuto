import csv
from pathlib import Path


def csv_reader(file, row_number):
    """
    Read a csv file
    """
    produits = []
    with open(Path("csv") / file, newline='') as csvfile:
        csv_produits = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in list(csv_produits)[1:]:
            produits.append(row[row_number])
    return produits


if __name__ == '__main__':
    print(csv_reader(file='Inventaire_Promocash.csv', row_number=0))