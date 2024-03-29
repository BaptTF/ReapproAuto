from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from csvReader import csv_reader
from csvWriter import csv_writer
from Create_Browser import create_browser
from time import sleep
from dotenv import load_dotenv
from os import getenv

def auchan(IDENTIFIANT_AUCHAN, PASSWORD_AUCHAN, WEB_BROWSER):
    # Récupération des courses à faire
    produits = csv_reader(file='Course.csv', row_number=0)
    nb_de_lots_a_acheter = csv_reader(file='Course.csv', row_number=1)
    nb_produits = csv_reader(file='Course.csv', row_number=2)
    supposed_nb_produits = csv_reader(file='Course.csv', row_number=3)
    nb_produits_par_lots = csv_reader(file='Course.csv', row_number=4)
    ref_produits_auchan = csv_reader(file='Course.csv', row_number=5)

    # Création du chrome en changeant sa taille parce que sinon le login marche pas
    driver = create_browser(WEB_BROWSER)

    # Authentification Auchan
    driver.get("https://www.auchan.fr/magasins/drive/laxou/s-875")
    driver.find_element(By.XPATH, "//button[contains(.,'Continuer sans accepter')]").click()
    sleep(1)
    driver.find_element(By.XPATH, "//button[contains(.,'Me connecter')]").click()
    driver.find_element(By.ID, "username").send_keys(IDENTIFIANT_AUCHAN)
    driver.find_element(By.ID, "password").send_keys(PASSWORD_AUCHAN)
    driver.find_element(By.XPATH, "//button[contains(.,'Se connecter')]").click()
    sleep(3)
    # Vérification que le Chariot est vide sinon on le vide
    driver.get("https://www.auchan.fr/checkout/cart/")
    sleep(2)
    try:
        driver.find_element(By.XPATH, "//button[contains(.,'Vider mon panier')]").click()
        sleep(1)
        driver.find_element(By.XPATH, "//button[@class='btn btn--small']").click()
        print("Le panier a été vidé")
    except:
        print("Le panier est déjà vide")
    prix = [('Produit', 'Nombre de lots à acheter', 'Nombre de produits par lots', 'Prix')]
    produits_non_trouves = [('Produit', 'Nombre de lots à acheter', 'Nombre de produits par lots', 'REF')]
    sleep(1)
    # Ajouts des produits
    def ajout_produit(row):
        driver.get(f"https://www.auchan.fr/recherche?text={ref_produits_auchan[row]}")
        sleep(0.5)
        try:
            prix_produit = float(driver.find_element(By.XPATH, "//meta[@itemprop='price']").get_attribute("content").replace(',','.'))
        except:
            print(f"Le produit {produits[row]} n'est pas était trouvé sur le drive, ajout dans le fichier Produits_non_trouves.csv")
            produits_non_trouves.append((produits[row], nb_de_lots_a_acheter[row], nb_produits_par_lots[row], ref_produits_auchan[row]))
            print("Passage au produit suivant")
            return
        prix.append((produits[row], nb_de_lots_a_acheter[row], nb_produits_par_lots[row], prix_produit))
        for i in range(int(nb_de_lots_a_acheter[row])):
            try:
                driver.find_element(By.XPATH, "//button[contains(.,'Ajouter au panier')]").click()
            except:
                print(f"Le produit {produits[row]} est au max, il y a {i+1} / {nb_de_lots_a_acheter[row]} mis dans le panier")
                prix[-1] = (produits[row], i + 1, nb_produits_par_lots[row], ref_produits_auchan[row])
                produits_non_trouves.append((produits[row], nb_de_lots_a_acheter[row] - i - 1, nb_produits_par_lots[row], ref_produits_auchan[row]))
                print(f"{nb_de_lots_a_acheter - i - 1} {produits[row]} ajouté dans le fichier Produits_non_trouves.csv")
                print("Passage au produit suivant")
                break
            sleep(0.5)

    for row in range(len(produits)):
        try:
            if ref_produits_auchan[row] != '':
                ajout_produit(row)
            else:
                print(f"Le produit {produits[row]} n'est pas disponible sur le drive, ajout dans le fichier produits_non_trouves.csv")
                produits_non_trouves.append((produits[row], nb_de_lots_a_acheter[row], nb_produits_par_lots[row], ref_produits_auchan[row]))
        except Exception as e:
            print(f"{produits[row]} n'as pas réussi à être ajouté à cause de l'erreur suivante : {e}")
            produits_non_trouves.append((produits[row], nb_de_lots_a_acheter[row], nb_produits_par_lots[row], ref_produits_auchan[row]))
            print(f"{produits[row]} ajouté dans le fichier Produits_non_trouves.csv")
            print("Passage au produit suivant")
        sleep(1)
    # Vérification du panier
    sleep(1)
    driver.get("https://www.auchan.fr/checkout/cart/")
    csv_writer('Prix.csv', prix)
    if produits_non_trouves != []:
        csv_writer('Produits_non_trouves.csv', produits_non_trouves)

if __name__ == '__main__':
    load_dotenv()
    auchan(getenv("IDENTIFIANT_AUCHAN"), getenv("PASSWORD_AUCHAN"), getenv("WEB_BROWSER"))
