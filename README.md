# ReapproAuto

## TLDR
Installer Google Chrome pour que ça marche
```bash
sudo apt install -y python3-venv;
```
```bash
source Install.sh
```
Puis REMPLISSER le fichier .env 
```
MONGO_MDP= <METTEZ ICI LE MDP DE LA BASE DE DONNÉES>
MONGO_PEM= <METTEZ LE CHEMIN ABSOLUE DU FICHIER PEM POUR SE CONNECTER A LA DB>
EMAIL= <METTEZ VOTRE ADDRESSE EMAIL AVEC @telecomancy.net>
PASSWORD_PROMOCASH= <METTEZ LE MDP DU PROMOCASH>
```
Puis REMPLISSER le fichier csv/Inventaire_Promocash.csv ou csv/Inventaire_Auchan.csv selon le réappro que vous voulez faire
```bash
source Start.sh
```

## PRESENTATION
Application Python qui utilise selenium et se connecte à la base de données pour faire le réapprovisionnement du bar

Ce programme automatise la réappro de openBar pour Promocash en plusieurs étapes décrites ci-dessous.

Chaque étape peut-être lancer individuellement dans leur fichier python respectif.

Le programme est résilient entre chaque étape car chaque étape génére un csv avec ses résultats donc si le programme plante au milieu d'une étape il est toujours possible de relancée à partir de là où vous vous êtes arrêter.

Le programme principale effectuant toutes les étapes se trouve dans le fichier RéaproComplete.py. 

Vous pouvez lancez le programme avec 
```bash
source Start.sh
```

### CONFIGURATION

Installer Google Chrome pour que ça marche

```bash
sudo apt install -y python3-venv;
```
Pour que le programme fonctionne il faut lancer ```Install.sh```
avec la commande 
```bash
source Install.sh 
```
Puis REMPLISSER le fichier .env 
```
MONGO_MDP= <METTEZ ICI LE MDP DE LA BASE DE DONNÉES>
MONGO_PEM= <METTEZ LE CHEMIN ABSOLUE DU FICHIER PEM POUR SE CONNECTER A LA DB>
EMAIL= <METTEZ VOTRE ADDRESSE EMAIL AVEC @telecomancy.net>
PASSWORD_PROMOCASH= <METTEZ LE MDP DU PROMOCASH>
```
Puis REMPLISSER le fichier csv/Inventaire.csv
Comme l'example ci dessous (nom produit, nombre dans le bar, nombre optimal dans le bar, nombre de produit par lot, moyen de chercher sur le drive)
```csv
Coca Cola,0,0,24,525199
```
La dernière colonne est utilisé pour cherche dans la barre de recherche du drive quel produit choisir

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