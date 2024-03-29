# Création du chrome en changeant sa taille parce que sinon le login marche pas
from selenium import webdriver

def create_browser(WEB_BROWSER):
    if WEB_BROWSER == "chrome":
        opts = webdriver.ChromeOptions()
        opts.add_argument("--window-size=1620,1000")
        opts.add_experimental_option("detach", True)
        try:
            driver = webdriver.Chrome(options=opts)
        except Exception as e:
            print(f"Le navigateur chrome n'est pas installé, erreur: {e}")
            print("Veuillez installer le navigateur chrome ou changer de navigateur dans le fichier .env")
            exit()

    elif WEB_BROWSER == "firefox":
        opts = webdriver.FirefoxOptions()
        opts.add_argument("--window-size=1620,1000")
        opts.set_preference('detach', True)
        try:
            driver = webdriver.Firefox(options=opts)
        except Exception as e:
            print(f"Le navigateur firefox n'est pas installé, erreur: {e}")
            print("Veuillez installer le navigateur firefox ou changer de navigateur dans le fichier .env")
            exit()
    else:
        print("Le navigateur n'est pas reconnu, veuillez choisir entre chrome et firefox")
        exit()
    driver.implicitly_wait(100)
    return driver

if __name__ == '__main__':
    create_browser("chrome")
    create_browser("firefox")
    print("All tests passed")