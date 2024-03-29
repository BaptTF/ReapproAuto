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

def updatePricePromocash(NUMERO_CARTE_PROMOCASH, PASSWORD_PROMOCASH, WEB_BROWSER):

    print("Les prix sont en train d'être mis à jour dans le fichier Prix.csv")
    # Récupération des prix
    produits = csv_reader(file='Prix.csv', row_number=0)
    nb_de_lots_a_acheter = csv_reader(file='Prix.csv', row_number=1)
    nb_produits_par_lots = csv_reader(file='Prix.csv', row_number=2)
    ifls_produits_promocash = csv_reader(file='Prix.csv', row_number=4)
    
    # Création du chrome en changeant sa taille parce que sinon le login marche pas
    driver = create_browser(WEB_BROWSER)

    print("Updating", end=" ")
    # Authentification Promocash
    driver.get("https://nancy.promocash.com/index.php")
    driver.find_element(By.XPATH, "//div[@id='monCompte']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CLI_NUMEROHeader"))).send_keys(NUMERO_CARTE_PROMOCASH)
    #driver.find_element(By.ID, "CLI_NUMEROHeader").send_keys(NUMERO_CARTE_PROMOCASH)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CLI_PASSWORDHeader"))).send_keys(PASSWORD_PROMOCASH)
    #driver.find_element(By.ID, "CLI_PASSWORDHeader").send_keys(PASSWORD_PROMOCASH)
    driver.find_element(By.ID, "submitValider").click()

    # Récupération des prix des produits
    def ajout_produit(row):
        driver.get(f"https://nancy.promocash.com/produitListe.php?searchString={ifls_produits_promocash[row]}")
        sleep(0.1)
        unit_prix = driver.find_element(By.XPATH, "//span[@class='unit']").text
        deci_prix = driver.find_element(By.XPATH, "//span[@class='deci']").text
        prix.append((produits[row],nb_de_lots_a_acheter[row], nb_produits_par_lots[row], float(unit_prix + "." + deci_prix), ifls_produits_promocash[row]))
        
    prix = []
    #print("Updating", end=" ")
    for row in range(len(produits)):
        if ifls_produits_promocash[row] != '' and produits[row] != "Bonbons Haribo":
            try:
                ajout_produit(row)
                print(".", end="")
            except:
                print(f"Le produit {produits[row]} n'a pas été ajouté car il n'a pas été trouvé sur le site de Promocash")
                print(f"Verifiez que le lien: https://nancy.promocash.com/produitListe.php?searchString={ifls_produits_promocash[row]}")
        else:
            print(f"Le produit {produits[row]} n'a pas été ajouté car il n'est pas dans la base de données")
    print("")
    csv_writer('Prix.csv', prix)

if __name__ == '__main__':
    load_dotenv()
    updatePricePromocash(getenv("NUMERO_CARTE_PROMOCASH"), getenv("PASSWORD_PROMOCASH"), getenv("WEB_BROWSER"))
#ajout_produit(0) 
# for row in range(len(produits)):
#     ajout_produit(row)

