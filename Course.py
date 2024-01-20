from csvReader import csv_reader
from csvWriter import csv_writer

# Récupération des produits et de le nombre
def creation_de_la_liste_de_course(seuil_pour_acheter_pourcentage_du_nombre_de_produits_par_lots, diff=False):
    produits = csv_reader(file='Inventaire.csv', row_number=0)
    nb_produits = csv_reader(file='Inventaire.csv', row_number=1)
    supposed_nb_produits = csv_reader(file='Inventaire.csv', row_number=2)
    nb_produits_par_lots = csv_reader(file='Inventaire.csv', row_number=3)
    ifls_produits_promocash = csv_reader(file='Inventaire.csv', row_number=4)
    #produits = [(p,nb,s) for p,nb,s in zip(produits,nb_produits, supposed_nb_produits)]

    course = []
    for i in range(len(produits)):
        if nb_produits[i] == 'Produit non trouvé': nb_produits[i] = 999999999
        nb_produits[i] = int(nb_produits[i])
        supposed_nb_produits[i] = int(supposed_nb_produits[i])
        nb_produits_par_lots[i] = int(nb_produits_par_lots[i])
        #print(produits[i], nb_produits[i], (seuil_pour_acheter_pourcentage_du_nombre_de_produits_par_lots / 100) * supposed_nb_produits[i])
        if nb_produits[i] < supposed_nb_produits[i] and nb_produits[i] < (seuil_pour_acheter_pourcentage_du_nombre_de_produits_par_lots / 100) * supposed_nb_produits[i]:
            nb_de_lots_a_acheter = 1 #((supposed_nb_produits[i] - nb_produits[i]) // nb_produits_par_lots[i]) + 1
            while nb_de_lots_a_acheter * nb_produits_par_lots[i] + nb_produits[i] < (seuil_pour_acheter_pourcentage_du_nombre_de_produits_par_lots / 100) * supposed_nb_produits[i]:
                nb_de_lots_a_acheter += 1
            course.append((produits[i], nb_de_lots_a_acheter, nb_produits[i], supposed_nb_produits[i], nb_produits_par_lots[i], ifls_produits_promocash[i]))
    if not diff:
        csv_writer('Course.csv', course)
    return course

def diff(course, seuil):
    csv_writer(f'CourseDiff{seuil}pourcent.csv', list(set(course) - set(creation_de_la_liste_de_course(seuil, True))))

if __name__ == '__main__':
    course = creation_de_la_liste_de_course(75)
    diff(course, 50)

