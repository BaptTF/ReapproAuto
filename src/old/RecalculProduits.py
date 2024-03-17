from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from time import sleep
from csvReader import csv_reader
from getpass import getpass
from test.Recalcul_prix import recalcul_prix
from dotenv import load_dotenv
from os import getenv

def RecalculProduits(EMAIL, PASSWORD):
    # Créer une instance du navigateur Chrome
    opts = webdriver.ChromeOptions()
    opts.add_argument("--window-size=1620,1000")
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(1)

    # Passez l'authentification Google
    driver.get("https://bar.telecomnancy.net/auth")
    driver.find_element(By.XPATH, "//*[@class='connect-button mt-4 svelte-107tmt3']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(EMAIL)
    #driver.find_element(By.ID, "identifierId").send_keys(EMAIL)
    driver.find_element(By.ID, "identifierNext").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(PASSWORD)
    #driver.find_element(By.NAME, "Passwd").send_keys(PASSWORD)
    driver.find_element(By.ID, "passwordNext").click()
    sleep(2)
    # Authentification passez avec succès
    print("Authentification réussie !")

    # Aller sur la page des produits
    driver.get("https://bar.telecomnancy.net/admin/produits")

    # Récupération des produits par nom
    def recalcul_produit_par_nom(name, prix):
        driver.find_element(By.XPATH, "//input[@placeholder='Rechercher']").send_keys(name)
        sleep(0.1)
        select_element = driver.find_element(By.XPATH, "//th[8]/select")
        select = Select(select_element)
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//th[8]/select")))
        for i in range(6):
            select.select_by_index(i)
            driver.find_element(By.ID, "price").send_keys(list(recalcul_prix(float(prix)).values())[i])
        select_element = driver.find_element(By.XPATH, "//td[4]/div/select")
        select = Select(select_element)
        sleep(0.1)
        select.select_by_index(0)
        print(name)
        driver.find_element(By.XPATH, "//input[@placeholder='Rechercher']").clear()

    produits = csv_reader(file='ProduitARecalculer.csv', row_number=0)
    prix = csv_reader(file='ProduitARecalculer.csv', row_number=1)
    for name, prix in zip(produits,prix):
        recalcul_produit_par_nom(name, prix)

if __name__ == '__main__':
    load_dotenv()
    RecalculProduits(getenv("EMAIL"), getpass('Password Google:'))