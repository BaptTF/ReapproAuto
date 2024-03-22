from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from csvReader import csv_reader
from csvWriter import csv_writer
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
    if WEB_BROWSER == "chrome":
        opts = webdriver.ChromeOptions()
        opts.add_argument("--window-size=1620,1000")
        opts.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=opts)
    elif WEB_BROWSER == "firefox":
        opts = webdriver.FirefoxOptions()
        opts.add_argument("--window-size=1620,1000")
        opts.set_preference('detach', True)
        driver = webdriver.Firefox(options=opts)
    driver.implicitly_wait(1)

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
    prix = []
    sleep(1)
    # Ajouts des produits
    def ajout_produit(row):
        driver.get(f"https://www.auchan.fr/recherche?text={ref_produits_auchan[row]}")
        sleep(0.5)
        try:
            prix_produit = float(driver.find_element(By.XPATH, "//meta[@itemprop='price']").get_attribute("content").replace(',','.'))
        except:
            print(f"Le produit {produits[row]} n'est pas disponible")
            return
        prix.append((produits[row],nb_de_lots_a_acheter[row], nb_produits_par_lots[row], prix_produit))
        for i in range(int(nb_de_lots_a_acheter[row])):
            try:
                driver.find_element(By.XPATH, "//button[contains(.,'Ajouter au panier')]").click()
            except:
                print(f"Le produit {produits[row]} est au max, il y a {i+1} / {nb_de_lots_a_acheter[row]} mis dans le panier")
                break
            sleep(0.5)
    for row in range(len(produits)):
        try:
            ajout_produit(row)
        except:
            print(f"Le produit {produits[row]} n'a pas été rajouté au panier")
        sleep(1)
    # Vérification du panier
    sleep(1)
    driver.get("https://www.auchan.fr/checkout/cart/")
    csv_writer('Prix.csv', prix)

if __name__ == '__main__':
    load_dotenv()
    auchan(getenv("IDENTIFIANT_AUCHAN"), getenv("PASSWORD_AUCHAN"), getenv("WEB_BROWSER"))
