# ReapproAuto

Application Python qui utilise selenium pour faire le réapprovisionnement du bar

Ce programme automatise la réappro de openBar pour Promocash en plusieurs décrites ci-dessous.

Chaque étape peut-être lancer individuellement dans leur fichier python respectif.

Le programme est résilient entre chaque étape car chaque étape génére un csv avec ses résultats donc si le programme plante au milieu d'une étape il est toujours possible de relancée à partir de là où vous vous êtes arrêter.

Le programme principale effectuant toutes les étapes se trouve dans le fichier RéaproComplete.py. L'avantage de lancée depuis RéaproComplete.py est que le mots de passe pour Google n'est demander qu'une fois

### CONFIGURATION

Pour que le programme fonctionne il faut crée un fichier config.py
```Python
EMAIL = "<prenom>.<nom>"
NUMERO_CARTE_PROMOCASH = "048104744"
```

Normalement le numéro de carte Promocash ne devrait pas avoir changer

Crée un venv
Pour cela entrer dans votre terminal la commande suivante
```Shell
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```
Vous pouvez maintenant executer le script principale
```Shell
python3 ReaproComplete.py
```

### INFORMATION IMPORTANTE

Tous ce script fonctionne avec selenium avec un navigateur il est donc logique que si les sites web en question changent le selenium ne fonctionne plus. Pour corriger cela à part changement majeur du site web il suffit simplement de changer les find_éléments pour qu'il récupérer les bons éléments

### 1 ERE ETAPE: FAIRE L'INVENTAIRE

La première étape est présente dans le fichier **inventaire.py** consiste à récupérer la quantité de chaque produit présent dans la première colonne du csv Inventaire.csv

### 2 EME ETAPE: CALCULER LES COURSES A FAIRE

La deuxième étape est présente dans le fichier **Course.py** consiste à calculer la liste de course à partir des quantités récupérer à étape 1 et aux quantitées supposées et d'un seuil en % qui réprensente le % minimum par rapport aux nombres supposés 

### 3 EME ETAPE: ALLER SUR PROMOCASH

La troisième étape est présente dans le fichier **Promocash.py** consiste à récupérer la liste de course dans le fichier Course.csv, d'ajouter dans le chariot tous les produits dans la liste de course et d'ajouter dans le chariot tous les produits qui ne sont pas au maximum dans le fichier Course_manuelle.csv.

Cette étape génére un csv Prix.csv qui contient tous les produits avec le nombre de produits achetés, le nombre de produits par lots, et le prix pour chaque lots.

### Question intermédiaire: Voulez-vous remettre le stock maximal pour course_manuelle ?

Cette étape intermédiare présente dans le fichier **remiseStockManuelle.py** est là pour remettre le fichier Course_manuelle.csv avec le nombre maximum possible en remplaçant le fichier Course_manuelle.csv par le fichier Course_manuelle_stock_max.csv

### 4 EME ETAPE: FAIRE LA REAPPRO SUR LE BAR

La quatrième étape est présente dans le fichier **Reappro.py** consiste à prendre tous les éléments dans le fichier Prix.csv pour remplir la réappro dans le bar. Cette étape récupérer aussi les anciens prix et les compare avec les nouveaux prix qu'il rentre.

Cette étape générer un fichier ProduitACacher.csv qui contients les produits qui ont changer de prix ainsi que la difference entre le nouveau prix et l'ancien prix.

### 5 EME ETAPE: CACHER LES PRODUITS QUI ONT CHANGE DE PRIX

La cinquième étape est présente dans le fichier **CacherProduits.py** consiste à prendre tous les produits dans le fichier ProduitsACacher.csv et à cacher tous ces produits dans le bar