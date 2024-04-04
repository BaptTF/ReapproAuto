import os
from pathlib import Path

def install():
    if not os.path.exists(Path(f"{os.path.dirname(__file__)}/.env")):
        with open(Path(f"{os.path.dirname(__file__)}/.env"), "w") as env:
            ans = input("Enter the threshold for the course (Optionnal) (press ENTER to skip): ")
            if not ans.isdigit():
                ans = 50
            env.write(f"""MONGO_MDP={input("Enter your MongoDB password (Obligatory): ")}
                        MONGO_PEM={input("Enter your absolute path to MongoDB PEM file (Obligatory): ")}
                        NUMERO_CARTE_PROMOCASH={input("Enter your Promocash card number (Optionnal) (press ENTER to skip): ")}
                        PASSWORD_PROMOCASH={input("Enter your Promocash password (Optionnal) (press ENTER to skip): ")}
                        IDENTIFIANT_AUCHAN={input("Enter your Auchan identifier (Optionnal) (press ENTER to skip): ")}
                        PASSWORD_AUCHAN={input("Enter your Auchan password (Optionnal) (press ENTER to skip): ")}
                        EMAIL={input("Enter your email in prenom.nom@telecomnancy.net (Obligatory): ")}
                        WEB_BROWSER={"chrome" if input("Enter your web browser (Obligatory) (firefox/chrome):") == "chrome" else "firefox"}
                        SEUIL_COURSE={ans}"""
                    )
            print(f"The parameters are in {os.path.dirname(__file__)}/.env file")
            print("If you want to change them, you can edit the file")
    else:
        print(f"The parameters are in {os.path.dirname(__file__)}/.env file")
        print("If you want to change them, you can edit the file")