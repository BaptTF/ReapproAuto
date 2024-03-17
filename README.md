# ReapproAuto

## TLDR
Avoir soit Firefox soit Google Chrome si possible installé avec apt parce que j'ai pas testé si ça fonctionne installé avec snap mais probablement pas mdr
https://doc.ubuntu-fr.org/firefox#installer_firefox_en_deb_classique_au_lieu_de_snap
```bash
sudo apt install -y python3-venv
```
```bash
source Install.sh
```
Puis REMPLISSER le fichier .env avec les information nécessaire pour votre réappro
<p>Obligatoire à remplir: MONGO_MDP, MONGO_PEM</p>
<p>Pour Promocash: NUMERO_CARTE_PROMOCASH, PASSWORD_PROMOCASH, WEB_BROWSER </p>
<p>Pour Auchan: IDENTIFIANT_AUCHAN, PASSWORD_AUCHAN, WEB_BROWSER</p>
<p>Pour faire une réappro dans le bar: EMAIL, WEB_BROWSER</p>

```
MONGO_MDP= <METTEZ ICI LE MDP DE LA BASE DE DONNÉES>
MONGO_PEM= <METTEZ LE CHEMIN ABSOLUE DU FICHIER PEM POUR SE CONNECTER A LA DB>
NUMERO_CARTE_PROMOCASH= <METTEZ VOTRE NUMERO DE CARTE PROMOCASH>
PASSWORD_PROMOCASH= <METTEZ LE MDP DU PROMOCASH>
IDENTIFIANT_AUCHAN= <METTEZ LE IDF DE AUCHAN>
PASSWORD_AUCHAN= <METTEZ LE PASSWORD AUCHAN>
EMAIL= <METTEZ VOTRE ADDRESSE EMAIL AVEC @telecomancy.net>
WEB_BROWSER= <METTEZ VOTRE NAVIGATEUR (chrome/firefox)>
```
Puis REMPLISSER le fichier csv/Inventaire_Promocash.csv ou csv/Inventaire_Auchan.csv selon le réappro que vous voulez faire
```bash
source Start.sh
```
Si vous êtes curieux de ce qu'est SEUIL_COURSE allez à la partie configuration

## PRESENTATION
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
Avoir soit Firefox soit Google Chrome si possible installé avec apt parce que j'ai pas testé si ça fonctionne installé avec snap mais probablement pas mdr
https://doc.ubuntu-fr.org/firefox#installer_firefox_en_deb_classique_au_lieu_de_snap
Le programme n'est fait que pour les produits à 5.5% de TVA pour l'instant
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
NUMERO_CARTE_PROMOCASH= <METTEZ VOTRE NUMERO DE CARTE PROMOCASH>
PASSWORD_PROMOCASH= <METTEZ LE MDP DU PROMOCASH>
IDENTIFIANT_AUCHAN= <METTEZ LE IDF DE AUCHAN>
PASSWORD_AUCHAN= <METTEZ LE PASSWORD AUCHAN>
EMAIL= <METTEZ VOTRE ADDRESSE EMAIL AVEC @telecomancy.net>
WEB_BROWSER= <METTEZ VOTRE NAVIGATEUR (chrome/firefox)>
SEUIL_COURSE=62.5
```

#### Explication de SEUIL_COURSE

SEUIL_COURSE est une constante qui sert à calculer les course à partir de de nombre de produit dans le bar et le nombre de produit par lot:
Un example sera plus parlant: <br>
Si on veut dans le bar 48 Coca Cola (montant optimal) et que dans le bar on a 47 Coca Cola on ne veut pas racheter 23 Coca en plus donc il faut un seuil à partir duquel on décide d'acheter le lot <br>
Le seuil est en pourcentage du nombre de produit par lots <br>
Le seuil par défaut est de 62.5 % en reprenant l'exemple au-dessus <br>
Il faut qu'il n'y 39 Coca dans le bar car 24 * 0.625 = 15 et 24 + 15 = 39 <br>
Ainsi si le seuil est de 100 % alors il faudra qu'il manque un lot complet pour en acheté un nouveau, example: 24 Coca pour 100 à SEUIL_COURSE <br>
Et si le seuil est de 0 % alors on achète dès qu'il manque un produit dans le bar cf le premier example <br>
Le seuil de 62,5 % un choix personnel que je trouvais plutôt bien mais reste réglable si vous voulez changer 

#### Explication de Inventaire_(Promocash/Auchan).csv

Le fichier csv/Inventaire_(Promocash/Auchan).csv

Comme l'example ci dessous (nom produit, nombre dans le bar, nombre optimal dans le bar, nombre de produit par lot, moyen de chercher sur le drive)
```csv
Coca Cola,0,0,24,525199
```
La dernière colonne est utilisé pour cherche dans la barre de recherche du drive quel produit choisir

#### Explication de Course.csv

(nom_produit, nb_de_lots_a_acheter, amount_left, optimal_amount, nb_produits_par_lots, ifls_produits_promocash ou ref_produits_auchan)
```csv
Coca Cherry,1,28,62,24,418172
```
Donc dans l'exemple ci-dessous on peut lire que: La liste course contient du Coca Cherry il faut en acheté 1 pack il y a 28 Coca Chery dans le bar actuellement, il faudrait en avoir 62 et le pack contient 24 Coca cherry, le numéro ou ref du produit dans le magasin

#### Explication de Prix.csv
(nom_produit, nb_de_lots_acheter, nb_produits_par_lots, prix)
```csv
Coca Cherry,1,24,15.12
```
On a acheté un pack de Coca Cherry pour 15.12 €

### INFORMATION IMPORTANTE

Tous ce script fonctionne avec selenium avec un navigateur il est donc logique que si les sites web en question changent le selenium ne fonctionne plus. Pour corriger cela à part changement majeur du site web il suffit simplement de changer les find_éléments pour qu'il récupérer les bons éléments 

### 1 ERE ETAPE: FAIRE L'INVENTAIRE

La première étape est présente dans le fichier **inventaireMongo.py** consiste à récupérer la quantité de chaque produit présent dans la première colonne du csv Inventaire.csv

### 2 EME ETAPE: CALCULER LES COURSES A FAIRE

La deuxième étape est présente dans le fichier **Course.py** consiste à calculer la liste de course à partir des quantités récupérer à étape 1 et aux quantitées supposées et d'un seuil en % qui réprensente le % minimum par rapport aux nombres supposés
Cette étape génére un fichier Course.csv qui contient la liste de course

### 3 EME ETAPE: ALLER SUR PROMOCASH OU AUCHAN

La troisième étape est présente dans le fichier **Promocash.py** ou **Auchan.py** consiste à récupérer la liste de course dans le fichier Course.csv, d'ajouter dans le chariot tous les produits dans la liste de course et d'ajouter dans le chariot tous les produits qui ne sont pas au maximum dans le fichier Course_manuelle.csv.

Cette étape génére un csv Prix.csv qui contient tous les produits avec le nombre de produits achetés, le nombre de produits par lots, et le prix pour chaque lots.

##### Question intermédiaire pour Promocash: Voulez-vous remettre le stock maximal pour course_manuelle ?

Cette étape intermédiare présente dans le fichier **remiseStockManuelle.py** est là pour remettre le fichier Course_manuelle.csv avec le nombre maximum possible en remplaçant le fichier Course_manuelle.csv par le fichier Course_manuelle_stock_max.csv

### 4 EME ETAPE: FAIRE LA REAPPRO SUR LE BAR

La réppro consiste à prendre tous les éléments dans le fichier Prix.csv pour remplir la réappro dans le bar.

Il y a 2 possibilités:
Soit la réappro avec le site du bar en utilisant Selenium Avantage: + plus de la réappro rentré Inconvenient: Utilise le navigateur pour rentrée la réappro
Présente dans le fichier **Reappro.py** 
Cette possibilité est un fonctionnalité expérimental n'ayant était testé que en dans un base de données local il est donc déconseiller de l'utiliser tant qu'elle n'as pas était testé correctement.
Soit la réppro en modifiant directement la base de données: Avantage: + rapide, +sûre qu'un navitageur Inconveniant: Si le programme bug au milieu c'est la merde notamment parce qu'on sait pas ce que ça a rentré.