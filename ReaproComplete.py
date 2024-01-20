from getpass import getpass
from inventaire import inventaire
from Course import creation_de_la_liste_de_course
from Promocash import promocash
from Reappro import reappro
from CacherProduits import cacher_produit
from remiseStockManuelle import stock_max

# Get the password only once
PASSWORD = getpass('Password Google:')

# 1 ERE ETAPE: FAIRE L'INVENTAIRE
inventaire(PASSWORD)

# 2 EME ETAPE: CALCULER LES COURSES A FAIRE
if input("Voulez-vous continuer à l'étape suivante ?") == 'y':
    creation_de_la_liste_de_course(62.5)
else:
    exit()

# 3 EME ETAPE: ALLER SUR PROMOCASH
if input("Voulez-vous continuer à l'étape suivante ?") == 'y':
    PASSWORD_PROMOCASH = getpass('Password Promocash:')
    promocash(PASSWORD_PROMOCASH)
else:
    exit()
# Question intermédiaire: Voulez-vous remettre le stock maximal pour course_manuelle ?
if input("Voulez-vous remettre le stock maximal pour course_manuelle ?") == 'y':
    stock_max()
else:
    print("Stock manuelle non modifié")
# 4 EME ETAPE: FAIRE LA REAPPRO SUR LE BAR
if input("Voulez-vous continuer à l'étape suivante ?") == 'y':
    reappro(PASSWORD)
else:
    exit()
# 5 EME ETAPE: CACHER LES PRODUITS QUI ONT CHANGE DE PRIX
if input("Voulez-vous continuer à l'étape suivante ?") == 'y':
    cacher_produit(PASSWORD)
else:
    exit()
