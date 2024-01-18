from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from getpass import getpass
from time import sleep
from csvReader import csv_reader
from csvWriter import csv_writer
from config import EMAIL

def reappro(PASSWORD):
    # Récupération des prix
    produits = csv_reader(file='Prix.csv', row_number=0)
    nb_de_lots_acheter = csv_reader(file='Prix.csv', row_number=1)
    nb_produits_par_lots = csv_reader(file='Prix.csv', row_number=2)
    prix = csv_reader(file='Prix.csv', row_number=3)

    # Création du chrome en changeant sa taille
    opts = webdriver.ChromeOptions()
    opts.add_argument("--window-size=1620,1000")
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(1)

    # Authentification Google
    driver.get("https://bar.telecomnancy.net/auth")
    driver.find_element(By.XPATH, "//*[@class='connect-button mt-4 svelte-107tmt3']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(EMAIL)
    #driver.find_element(By.ID, "identifierId").send_keys(EMAIL)
    driver.find_element(By.ID, "identifierNext").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(PASSWORD)
    #driver.find_element(By.NAME, "Passwd").send_keys(PASSWORD)
    driver.find_element(By.ID, "passwordNext").click()
    sleep(2)

    # Aller sur la page des Réapprovisionnements
    produit_a_cacher = []
    driver.get("https://bar.telecomnancy.net/panel/products/reappro")
    def ajout_produit(row, marge):
        driver.find_element(By.XPATH, "//input[@placeholder='Nom du produit']").send_keys(produits[row])
        driver.find_element(By.XPATH, "//div[2]/button").click()
        driver.find_element(By.XPATH, "//input[@placeholder='Nombre de lots']").send_keys(Keys.BACKSPACE)
        driver.find_element(By.XPATH, "//input[@placeholder='Nombre de lots']").send_keys(nb_de_lots_acheter[row])
        driver.find_element(By.XPATH, "//input[@placeholder='Nombre de produits par lots']").send_keys(Keys.BACKSPACE)
        driver.find_element(By.XPATH, "//input[@placeholder='Nombre de produits par lots']").send_keys(nb_produits_par_lots[row])
        driver.find_element(By.XPATH, "//td[6]/div/input").click()
        vieux_prix = driver.find_element(By.XPATH, "//td[6]/div/input").get_attribute("placeholder")[:-2]
        select_element = driver.find_element(By.XPATH, "//td[7]/div/select")
        select = Select(select_element)
        select.select_by_index(1)
        driver.find_element(By.XPATH, "//td[6]/div/input").send_keys(prix[row])
        driver.find_element(By.XPATH, "//button[contains(.,'Ajouter')]").click()
        difference = abs(float(vieux_prix) - float(prix[row]))
        if difference >= marge:
            produit_a_cacher.append((produits[row], difference))

    for row in range(len(produits)):
        ajout_produit(row, 0.05)

    # Cacher les produits qui ont changé de prix
    csv_writer("ProduitACacher.csv", produit_a_cacher)

if __name__ == '__main__':
    PASSWORD = getpass('Password Google:')
    reappro(PASSWORD)
