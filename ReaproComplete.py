from getpass import getpass
from inventaire import inventaire
from Course import creation_de_la_liste_de_course
from Promocash import promocash
from Reappro import reappro
from CacherProduits import cacher_produit

# Get the password only once
PASSWORD = getpass('Password Google:')

# 1 ERE ETAPE: FAIRE L'INVENTAIRE
inventaire(PASSWORD)

# 2 EME ETAPE: CALCULER LES COURSES A FAIRE
if input("Voulez-vous continuer à l'étape suivante ?") == 'y':
    creation_de_la_liste_de_course(75)
else:
    exit()

# 3 EME ETAPE: ALLER SUR PROMOCASH
if input("Voulez-vous continuer à l'étape suivante ?") == 'y':
    PASSWORD_PROMOCASH = getpass('Password Promocash:')
    promocash(PASSWORD_PROMOCASH)
else:
    exit()

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
