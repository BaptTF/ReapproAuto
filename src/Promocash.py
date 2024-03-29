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

def promocash(NUMERO_CARTE_PROMOCASH, PASSWORD_PROMOCASH, WEB_BROWSER):
    # Récupération des courses à faire
    produits = csv_reader(file='Course.csv', row_number=0)
    nb_de_lots_a_acheter = csv_reader(file='Course.csv', row_number=1)
    nb_produits = csv_reader(file='Course.csv', row_number=2)
    supposed_nb_produits = csv_reader(file='Course.csv', row_number=3)
    nb_produits_par_lots = csv_reader(file='Course.csv', row_number=4)
    ifls_produits_promocash = csv_reader(file='Course.csv', row_number=5)

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


    # Authentification Promocash
    driver.get("https://nancy.promocash.com/index.php")
    driver.find_element(By.XPATH, "//div[@id='monCompte']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CLI_NUMEROHeader"))).send_keys(NUMERO_CARTE_PROMOCASH)
    #driver.find_element(By.ID, "CLI_NUMEROHeader").send_keys(NUMERO_CARTE_PROMOCASH)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CLI_PASSWORDHeader"))).send_keys(PASSWORD_PROMOCASH)
    #driver.find_element(By.ID, "CLI_PASSWORDHeader").send_keys(PASSWORD_PROMOCASH)
    driver.find_element(By.ID, "submitValider").click()

    # Ajouts des produits
    def ajout_produit(row):
        driver.get(f"https://nancy.promocash.com/produitListe.php?searchString={ifls_produits_promocash[row]}")
        nb_de_lots_int = int(nb_de_lots_a_acheter[row])
        sleep(0.1)
        for _ in range(nb_de_lots_int - 1):
            driver.find_element(By.XPATH, "//a[@class='pictoPlus']").click()
        unit_prix = driver.find_element(By.XPATH, "//span[@class='unit']").text
        deci_prix = driver.find_element(By.XPATH, "//span[@class='deci']").text
        prix.append((produits[row],nb_de_lots_a_acheter[row], nb_produits_par_lots[row], float(unit_prix + "." + deci_prix), ifls_produits_promocash[row]))
        driver.find_element(By.XPATH, "//input[@value='Commander']").click()

    # Vérification que le Chariot est vide sinon on le vide
    driver.get("https://nancy.promocash.com/cmdEtape1.php")
    sleep(1)
    try:
        driver.find_element(By.ID, "viderPanier").click()
        alert = driver.switch_to.alert
        alert.accept()
        print("Le panier a été vidé")
    except:
        print("Le panier était déjà vide")
    sleep(0.2)
    prix = []
    for row in range(len(produits)):
        if ifls_produits_promocash[row] != '' and produits[row] != "Bonbons Haribo":
            ajout_produit(row)
        else:
            print(f"Le produit {produits[row]} n'a pas été ajouté car il n'est pas dans la base de données")

    csv_writer('Prix.csv', prix)


    ##########################
    # Partie Course_manuelle #
    ##########################


    produits = csv_reader('Course_manuelle.csv', row_number=0)
    nb_produits = csv_reader('Course_manuelle.csv', row_number=1)
    supposed_nb_produits = csv_reader('Course_manuelle.csv', row_number=2)
    ifls_produits_promocash = csv_reader('Course_manuelle.csv', row_number=3)
    prix_manuelle = []
    def ajout_produit(row):
        driver.get(f"https://nancy.promocash.com/produitListe.php?searchString={ifls_produits_promocash[row]}")
        nb_de_lots_int = int(supposed_nb_produits[row]) -  int(nb_produits[row])
        while nb_de_lots_int > 1:
            driver.find_element(By.XPATH, "//a[@class='pictoPlus']").click()
            nb_de_lots_int -= 1
        unit_prix = driver.find_element(By.XPATH, "//span[@class='unit']").text
        deci_prix = driver.find_element(By.XPATH, "//span[@class='deci']").text
        prix_manuelle.append((produits[row],int(supposed_nb_produits[row]) -  int(nb_produits[row]), float(unit_prix + "." + deci_prix), ifls_produits_promocash[row]))
        driver.find_element(By.XPATH, "//input[@value='Commander']").click()

    for row in range(len(produits)):
        if ifls_produits_promocash[row] != '' and int(supposed_nb_produits[row]) -  int(nb_produits[row]) > 0:
            ajout_produit(row)
    if prix_manuelle != []:
        prix_manuelle.append(("Total HT",sum([x[2] for x in prix_manuelle])))
    else:
        prix_manuelle.append(("Total HT",0))
    csv_writer('Prix_manuelle.csv', prix_manuelle)
    driver.get("https://nancy.promocash.com/cmdEtape1.php")

if __name__ == '__main__':
    load_dotenv()
    promocash(getenv("NUMERO_CARTE_PROMOCASH"), getenv("PASSWORD_PROMOCASH"), getenv("WEB_BROWSER"))
#ajout_produit(0) 
# for row in range(len(produits)):
#     ajout_produit(row)

