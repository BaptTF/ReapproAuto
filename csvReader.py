import csv


def csv_reader(file, row_number):
    """
    Read a csv file
    """
    produits = []
    with open(file, newline='') as csvfile:
        csv_produits = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_produits:
            produits.append(row[row_number])
    return produits


if __name__ == '__main__':
    print(csv_reader(file='Inventaire.csv', row_number=0))