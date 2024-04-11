from csvReader import csv_reader
from csvWriter import csv_writer

def calcul_ttc_prix_promocash():

    produits = csv_reader(file='Prix_test.csv', row_number=0)
    nb_de_lots_acheter = csv_reader(file='Prix_test.csv', row_number=1)
    nb_produits_par_lots = csv_reader(file='Prix_test.csv', row_number=2)
    prix = csv_reader(file='Prix_test.csv', row_number=3)
    ref = csv_reader(file='Prix_test.csv', row_number=4)

    sum_ttc = 0
    sum_ht = 0
    prix_ttc_test = [('Produit', 'Nombre de lots à acheter', 'Nombre de produits par lots', 'Prix', 'REF')]
    for row in range(len(produits)):
        sum_ht += float(prix[row]) * int(nb_de_lots_acheter[row])
        if produits[row] != "Bonbons Haribo":
            prix_ttc = float(prix[row]) * int(nb_de_lots_acheter[row]) * 1.055
        else:
            prix_ttc = float(prix[row]) * int(nb_de_lots_acheter[row]) * 1.2
        sum_ttc += prix_ttc
        prix_ttc_test.append((produits[row], nb_de_lots_acheter[row], nb_produits_par_lots[row], round(prix_ttc, 2), ref[row]))
    
    prix_ttc_test.append(("Total HT", sum_ht))
    prix_ttc_test.append(("Total TTC", sum_ttc))
    print(sum_ht)
    print(round(sum_ttc, 2))
    print(f"Total HT : {round(sum([float(prix[i]) * int(nb_de_lots_acheter[i]) for i in range(len(produits))]),2):.2f}")
    csv_writer('Prix_ttc_test.csv', prix_ttc_test)

if __name__ == '__main__':
    calcul_ttc_prix_promocash()
