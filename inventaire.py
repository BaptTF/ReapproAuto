from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from csvReader import csv_reader
from csvWriter import csv_writer
from config import EMAIL
from getpass import getpass

# Get the password
def inventaire(PASSWORD):
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
    def recup_produit_par_nom(name):
        driver.find_element(By.XPATH, "//input[@placeholder='Rechercher']").send_keys(name)
        #sleep(1)
        try:
            nb_produit = driver.find_element(By.XPATH, "//td[5]/div/input").get_attribute("value")
            if nb_produit == "0":
                sleep(1)
                nb_produit = driver.find_element(By.XPATH, "//td[5]/div/input").get_attribute("value")
        except NoSuchElementException:
            nb_produit = "Produit non trouvé"
        print(name, nb_produit)
        driver.find_element(By.XPATH, "//input[@placeholder='Rechercher']").clear()
        return nb_produit
    nb_tous_produits = []
    produits = csv_reader(file='Inventaire.csv', row_number=0)
    supposed_nb_produits = csv_reader(file='Inventaire.csv', row_number=2)
    nb_produits_par_lots = csv_reader(file='Inventaire.csv', row_number=3)
    ifls_produits_promocash = csv_reader(file='Inventaire.csv', row_number=4)
    for name in produits:
        nb_tous_produits.append(recup_produit_par_nom(name))
    csv_writer('Inventaire.csv', [(p, ntp, snp, nppl, ipp) for p, ntp, snp, nppl, ipp in zip(produits, nb_tous_produits, supposed_nb_produits, nb_produits_par_lots, ifls_produits_promocash)])

if __name__ == '__main__':
    inventaire(getpass('Password:'))