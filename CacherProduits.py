from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from time import sleep
from csvReader import csv_reader
from config import EMAIL
from getpass import getpass

def cacher_produit(PASSWORD):
    # Créer une instance du navigateur Chrome
    driver = webdriver.Chrome()
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
    def cacher_produit_par_nom(name):
        driver.find_element(By.XPATH, "//input[@placeholder='Rechercher']").send_keys(name)
        sleep(0.1)
        select_element = driver.find_element(By.XPATH, "//td[4]/div/select")
        select = Select(select_element)
        select.select_by_index(1)
        print(name)
        driver.find_element(By.XPATH, "//input[@placeholder='Rechercher']").clear()

    produits = csv_reader(file='ProduitACacher.csv', row_number=0)
    for name in produits:
        cacher_produit_par_nom(name)

if __name__ == '__main__':
    cacher_produit(getpass('Password Google:'))