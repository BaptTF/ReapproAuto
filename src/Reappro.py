from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from getpass import getpass
from time import sleep
from csvReader import csv_reader
from dotenv import load_dotenv
from os import getenv

def reappro(EMAIL, PASSWORD, WEB_BROWSER, magasin):
    if magasin == "p":
        input_price = 6
    elif magasin == "a":
        input_price = 8
    # Récupération des prix
    produits = csv_reader(file='Prix.csv', row_number=0)
    nb_de_lots_acheter = csv_reader(file='Prix.csv', row_number=1)
    nb_produits_par_lots = csv_reader(file='Prix.csv', row_number=2)
    prix = csv_reader(file='Prix.csv', row_number=3)

    # Création du chrome en changeant sa taille
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

    # Authentification Google
    driver.get("https://bar.telecomnancy.net/auth")
    driver.find_element(By.XPATH, "//*[@class='connect-button mt-4 svelte-107tmt3']").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "identifierId"))).send_keys(EMAIL)
    #driver.find_element(By.ID, "identifierId").send_keys(EMAIL)
    driver.find_element(By.ID, "identifierNext").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(PASSWORD)
    #driver.find_element(By.NAME, "Passwd").send_keys(PASSWORD)
    driver.find_element(By.ID, "passwordNext").click()
    sleep(2)
    # Aller sur la page des Réapprovisionnements
    driver.get("https://bar.telecomnancy.net/panel/products/reappro")
    def ajout_produit(row):
        if produits[row][-1] == '$':
            driver.find_element(By.XPATH, "//input[@placeholder='Nom du produit']").send_keys(produits[row][:-1])
            driver.find_element(By.XPATH, "//input[@placeholder='Nom du produit']").send_keys("$")
        else:
            driver.find_element(By.XPATH, "//input[@placeholder='Nom du produit']").send_keys(produits[row])
        sleep(2)
        driver.find_element(By.XPATH, "//div[2]/button").click()
        sleep(2)
        driver.find_element(By.XPATH, "//input[@placeholder='Nombre de lots']").send_keys(Keys.BACKSPACE)
        driver.find_element(By.XPATH, "//input[@placeholder='Nombre de lots']").send_keys(nb_de_lots_acheter[row])
        driver.find_element(By.XPATH, "//input[@placeholder='Nombre de produits par lots']").send_keys(Keys.BACKSPACE)
        driver.find_element(By.XPATH, "//input[@placeholder='Nombre de produits par lots']").send_keys(nb_produits_par_lots[row])
        driver.find_element(By.XPATH, "//td[6]/div/input").click()
        sleep(0.1)
        select_element = driver.find_element(By.XPATH, "//td[7]/div/select")
        select = Select(select_element)
        select.select_by_index(1)
        driver.find_element(By.XPATH, f"//td[{input_price}]/div/input").send_keys(prix[row])
        driver.find_element(By.XPATH, "//button[contains(.,'Ajouter')]").click()

    for row in range(len(produits)):
        ajout_produit(row)
        sleep(0.2)


if __name__ == '__main__':
    PASSWORD = getpass('Password Google:')
    load_dotenv()
    reappro(getenv("EMAIL"), PASSWORD, getenv("WEB_BROWSER"),"a")
