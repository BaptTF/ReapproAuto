from csvReader import csv_reader

def print_calcul_prix_total(magasin):
    try:
        produits = csv_reader(file='Prix.csv', row_number=0)
        nb_de_lots_acheter = csv_reader(file='Prix.csv', row_number=1)
        prix = csv_reader(file='Prix.csv', row_number=3)
    except FileNotFoundError:
        print("Le fichier Prix.csv n'existe pas, veuillez faire la reappro avant de continuer")
        exit()
    if magasin == "p":
        # Un meilleur calcul serait sum(float(prix[i]) * 100 * int(nb_de_lots_acheter[i])) / 100 mais promocash fait les calculs comme ça mdr
        print(f"Total HT : {round(sum([float(prix[i]) * int(nb_de_lots_acheter[i]) for i in range(len(produits))]),2):.2f}")
    elif magasin == "a":
        print("Attention le calcul TTC est basé sur une tva de 5.5% pour tous les produits")
        print(f"Total TTC : {round(sum([float(prix[i])*1.055 * int(nb_de_lots_acheter[i]) for i in range(len(produits))]),2):.2f}")
    elif magasin == "all":
        # Un meilleur calcul serait sum(float(prix[i]) * 100 * int(nb_de_lots_acheter[i])) / 100 mais promocash fait les calculs comme ça mdr
        print(f"Total HT : {round(sum([float(prix[i]) * int(nb_de_lots_acheter[i]) for i in range(len(produits))]),2):.2f}")
        print("Attention le calcul TTC est basé sur une tva de 5.5% pour tous les produits")
        print(f"Total TTC : {round(sum([float(prix[i])*1.055 * int(nb_de_lots_acheter[i]) for i in range(len(produits))]),2):.2f}")
    else:
        print("Drive inconnu")
        exit()

if __name__ == '__main__':
    print_calcul_prix_total("all")