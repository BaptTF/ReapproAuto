from csvReader import csv_reader
from csvWriter import csv_writer

def stock_max():
    produits = csv_reader('Course_manuelle_stock_max.csv', row_number=0)
    nb_produits = csv_reader('Course_manuelle_stock_max.csv', row_number=1)
    supposed_nb_produits = csv_reader('Course_manuelle_stock_max.csv', row_number=2)
    ifls_produits_promocash = csv_reader('Course_manuelle_stock_max.csv', row_number=3)

    csv_writer("Course_manuelle.csv", [(p, nb, s, i) for p, nb, s, i in zip(produits, nb_produits, supposed_nb_produits, ifls_produits_promocash)])

if __name__ == '__main__':
    stock_max()