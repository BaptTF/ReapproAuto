import os
from pathlib import Path

def install():
    if not os.path.exists(Path(f"{os.path.dirname(__file__)}/.env")):
        with open(Path(f"{os.path.dirname(__file__)}/.env"), "w") as env:
            env.write(f"""MONGO_MDP={input("Enter your MongoDB password: ")}
                        MONGO_PEM={input("Enter your abs path to MongoDB PEM file: ")}
                        NUMERO_CARTE_PROMOCASH={input("Enter your Promocash card number: ")}
                        PASSWORD_PROMOCASH={input("Enter your Promocash password: ")}
                        IDENTIFIANT_AUCHAN={input("Enter your Auchan identifier: ")}
                        PASSWORD_AUCHAN={input("Enter your Auchan password: ")}
                        EMAIL={input("Enter your email in prenom.nom@telecomnancy.net: ")}
                        WEB_BROWSER=firefox
                        SEUIL_COURSE=50"""
                    )
            print(f"The parameter are in {os.path.dirname(__file__)}/.env file")
    else:
        print(f"The parameter are in {os.path.dirname(__file__)}/.env file")