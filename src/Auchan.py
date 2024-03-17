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

def auchan(IDENTIFIANT_AUCHAN, PASSWORD_AUCHAN):
    # Récupération des courses à faire
    produits = csv_reader(file='Course.csv', row_number=0)
    nb_de_lots_a_acheter = csv_reader(file='Course.csv', row_number=1)
    nb_produits = csv_reader(file='Course.csv', row_number=2)
    supposed_nb_produits = csv_reader(file='Course.csv', row_number=3)
    nb_produits_par_lots = csv_reader(file='Course.csv', row_number=4)
    ref_produits_auchan = csv_reader(file='Course.csv', row_number=5)

    # Création du chrome en changeant sa taille parce que sinon le login marche pas
    opts = webdriver.ChromeOptions()
    opts.add_argument("--window-size=1620,1000")
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(1)

    # Authentification Auchan
    driver.get("https://www.auchan.fr/magasins/drive/laxou/s-875")
    driver.find_element(By.XPATH, "//button[contains(.,'Continuer sans accepter')]").click()
    driver.find_element(By.XPATH, "//button[contains(.,'Me connecter')]").click()
    driver.find_element(By.ID, "username").send_keys(IDENTIFIANT_AUCHAN)
    driver.find_element(By.ID, "password").send_keys(PASSWORD_AUCHAN)
    driver.find_element(By.XPATH, "//button[contains(.,'Se connecter')]").click()
    sleep(1)
    # Vérification que le Chariot est vide sinon on le vide
    driver.get("https://www.auchan.fr/checkout/cart/")
    sleep(1)
    try:
        driver.find_element(By.XPATH, "//button[contains(.,'Vider mon panier')]").click()
        sleep(1)
        driver.find_element(By.XPATH, "//button[@class='btn btn--small']").click()
        print("Le panier a été vidé")
    except:
        print("Le panier est déjà vide")
    prix = []
    # Ajouts des produits
    def ajout_produit(row):
        driver.find_element(By.NAME, "text").send_keys(ref_produits_auchan[row])
        driver.find_element(By.NAME, "text").send_keys(Keys.ENTER)
        prix_produit = float(driver.find_element(By.XPATH, "//meta[@itemprop='price']").get_attribute("content").replace(',','.'))
        prix.append((produits[row],nb_de_lots_a_acheter[row], nb_produits_par_lots[row], prix_produit))
        for _ in range(int(nb_de_lots_a_acheter[row])):
            driver.find_element(By.XPATH, "//button[contains(.,'Ajouter au panier')]").click()
            sleep(0.1)
        driver.find_element(By.NAME, "text").clear()
    for row in range(len(produits)):
        ajout_produit(row)
        sleep(1)
    # Vérification du panier
    sleep(1)
    driver.get("https://www.auchan.fr/checkout/cart/")
    csv_writer('Prix.csv', prix)

if __name__ == '__main__':
    load_dotenv()
    auchan(getenv("IDENTIFIANT_AUCHAN"), getenv("PASSWORD_AUCHAN"))
