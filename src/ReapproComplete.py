from getpass import getpass
from inventaireMongo import inventaire_mongo
from Course import creation_de_la_liste_de_course
from Promocash import promocash
from Auchan import auchan
from Reappro import reappro
from ReapproMongo import reappro_mongo
from remiseStockManuelle import stock_max
from UpdatePricePromocash import updatePricePromocash
from PrintCalculPrixTotal import print_calcul_prix_total
from CalculOptimalAmount import calcul_optimal_amount
from UpdateOptimalAmount import update_optimal_amount
from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv

# Load the environment variables
load_dotenv(override=True)

# 1 ERE ETAPE: FAIRE L'INVENTAIRE
# Create a MongoClient object and specify the connection URL
client = MongoClient(f"mongodb://bar:{getenv('MONGO_MDP')}@mongo.telecomnancy.net:443/?authMechanism=DEFAULT&authSource=bar&directConnection=true&tls=true&tlsCertificateKeyFile={getenv('MONGO_PEM')}")
magasin = input("Course pour Promocash ou pour Auchan ou passez à l'étape de la réappro si vous avez déjà fait vos courses (p/a/r/u) ?")
if magasin == 'p' or magasin == 'a':
    file = "Inventaire_Promocash.csv" if magasin == 'p' else "Inventaire_Auchan.csv"
    last_row = "ifls_produits_promocash" if magasin == 'p' else "ref_produits_auchan"
    if magasin == 'p':
        inventaire_mongo(client, file)
    else:
        inventaire_mongo(client, file)

    print(f"Inventaire fait dans le fichier {file} (nom_produit, amount_left, optimal_amount, nb_produits_par_lots, {last_row}")

    # 2 EME ETAPE: CALCULER LES COURSES A FAIRE
    if magasin == 'p':
        creation_de_la_liste_de_course(float(getenv("SEUIL_COURSE")), file)
    else:
        creation_de_la_liste_de_course(float(getenv("SEUIL_COURSE")), file)
    print(f"Course calculer dans le fichier Course.csv (nom_produit, nb_de_lots_a_acheter, amount_left, optimal_amount, nb_produits_par_lots, {last_row})")
    print(f"Course non drive calculer dans le fichier Course_non_drive.csv (nom_produit, nb_de_lots_a_acheter, amount_left, optimal_amount, nb_produits_par_lots)")

    if magasin == 'p':
        # 3 EME ETAPE: ALLER SUR PROMOCASH
        if input("Voulez-vous commander sur Promocash (y/n) ?") == 'y':
            promocash(getenv("NUMERO_CARTE_PROMOCASH"), getenv("PASSWORD_PROMOCASH"), getenv("WEB_BROWSER"))
            print("Commande faite sur Promocash et enregistré le fichier Prix.csv (nom_produit, nb_de_lots_acheter, nb_produits_par_lots, prix)")
            print("Les produits non trouvés sont dans le fichier Produits_non_trouves.csv")
            print_calcul_prix_total(magasin)
        else:
            exit()
    else:
        # 3 EME ETAPE: ALLER SUR AUCHAN
        if input("Voulez-vous commander sur Auchan (y/n) ?") == 'y':
            auchan(getenv("IDENTIFIANT_AUCHAN"), getenv("PASSWORD_AUCHAN"), getenv("WEB_BROWSER"))
            print("Commande faite sur Auchan et enregistré le fichier Prix.csv (nom_produit, nb_de_lots_acheter, nb_produits_par_lots, prix)")
            print("Les produits non trouvés sont dans le fichier Produits_non_trouves.csv")
            print_calcul_prix_total(magasin)
        else:
            exit()

    if magasin == 'p':
        # Question intermédiaire: Voulez-vous remettre le stock maximal pour course_manuelle ?
        if input("Voulez-vous remettre le stock maximal pour course_manuelle (y/n) ?") == 'y':
            stock_max()
            print("Stock manuelle remis à jour")
        else:
            print("Stock manuelle non modifié")
elif magasin == 'r':
    # 4 EME ETAPE: FAIRE LA REAPPRO SUR LE BAR
    print_calcul_prix_total("all")
    magasin = input("Voulez-vous faire la reappro pour Promocash ou pour Auchan (p/a) ?")
    if magasin == 'p':
        if input("Voulez-vous mettre à jour les prix sur Promocash (y/n) ?") == 'y':
            updatePricePromocash(getenv("NUMERO_CARTE_PROMOCASH"), getenv("PASSWORD_PROMOCASH"), getenv("WEB_BROWSER"))
            print("Les prix ont été mis à jour dans le fichier Prix.csv")
    ans = input("Voulez-vous utiliser la reappro via la base de données directement ou par le site du bar ? (bar/bd)" )
    if ans == "bar":
        if input("Etes-vous sûre de vouloir faire la reappro avec le site du bar? (y/n)") == 'y':
            # Get the password for the Google account
            PASSWORD = getpass('Password Google de votre compte TN.net:')
            reappro(getenv("EMAIL"), PASSWORD, getenv("WEB_BROWSER"), magasin)
            print("Reappro fait sur le site du bar")
        else:
            exit()
    elif ans == "bd":
        # Ici le choix de promocash / auchan décide si on fait calcul la tva pour les prix ou non en fonction de last_tva
        print("Cette fonctionnalité est expérimentale et peut corrompre la base de données, veuillez vérifier les données avant de continuer")
        if input("Etes-vous sûre de vouloir faire la reappro via la base données directement (y/n) ?") == 'y':
            reappro_mongo(client, getenv("EMAIL"), magasin)
            print("Reappro fait via la base de données directement")
        else:
            exit()
elif magasin == 'u':
    # 5 EME ETAPE: CALCULER LE NOMBRE OPTIMAL DE PRODUITS
    magasin = input("Voulez-vous calculer le nombre optimal de produits pour Promocash ou pour Auchan (p/a) ?")
    if magasin == 'p':
        calcul_optimal_amount(client, magasin)
    elif magasin == 'a':
        calcul_optimal_amount(client, magasin)
    else:
        print("Drive inconnue")
    
    # 6 EME ETAPE: METTRE A JOUR LE NOMBRE OPTIMAL DE PRODUITS
    magasin = input("Voulez-vous mettre à jour le nombre optimal de produits (y/n) ?")
    if magasin == 'y':
        update_optimal_amount(client, "Update_optimal.csv", security=False)
    elif magasin == 'n':
        print("Le nombre optimal de produits n'a pas été mis à jour")
    else:
        print("Commande inconnue, Le nombre optimal de produits n'a pas été mis à jour")
else:
    print("Commande inconnue")

    # Close the connection when you're done
client.close()