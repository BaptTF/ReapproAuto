from csvReader import csv_reader
from csvWriter import csv_writer
from pymongo import MongoClient
from time import time
from uuid import uuid4
from os import getenv
from dotenv import load_dotenv
from bson.int64 import Int64
from Recalcul_prix_centimes import recalcul_prix_centimes

def reappro_mongo(client, email, magasin):
    print("Attention, cette fonction est dangereuse, elle modifie la base de donnée du bar")
    security = input("La réappro ce base sur le fichier Prix.csv êtes vous sûre que c'est la bonne réappro? (y/n)")
    if security != "y":
        print("Reappro annulé")
        exit()
    print("Si tu utilise cette fonctionnalité c'est que tu es sûr de ce que tu fais, sinon tu risque de tout casser, tu es sûr de ce que tu fais?")
    second_security = input("Je suis responsable de ma reappro, je suis sûr de ce que je fais (y/n)")
    if second_security != "y":
        print("Reappro annulé")
        exit()
    produits = csv_reader(file='Prix.csv', row_number=0)
    nb_de_lots_acheter = csv_reader(file='Prix.csv', row_number=1)
    nb_produits_par_lots = csv_reader(file='Prix.csv', row_number=2)
    prix = csv_reader(file='Prix.csv', row_number=3)

    collection_restocks = client["bar"]["restocks"]
    #print(list(collection.find()))
    usr = client["bar"]["accounts"].find_one({"email_address": email})

    Reappro = { 
                "created_by": usr["id"],
                "created_by_name": usr["first_name"] + " " + usr["last_name"],
                "deleted_at": None,
                "deleted_by": None,
                "driver_id": None,
                "driver_name": None,
                "id": uuid4().bytes,
                "items": [],
                "total_cost_ht": 0,
                "total_cost_ttc": 0,
                "type": "promocash",
                "created_at": Int64(time()),
                }
    for i in range(len(produits)):
        query = { "name": { "$regex": produits[i], "$options" :'i' }}
        collection_item = client["bar"]["items"]
        item = collection_item.find_one(query)
        if item == None:
            print(f"{produits[i]} non trouvé")
            continue
        prix_centimes = Int64(float(prix[i])*100)
        if magasin == "p":
            prix_centimes_tva = round(prix_centimes * 1.055)
        elif magasin == "a":
            prix_centimes_tva = prix_centimes
        all_prices = recalcul_prix_centimes(round(prix_centimes_tva / (int(nb_de_lots_acheter[i]) * int(nb_produits_par_lots[i]))))
        newvalues = { "$set": { 
            "amount_left":  Int64(item["amount_left"] + int(nb_de_lots_acheter[i]) * int(nb_produits_par_lots[i])),
            "prices": {
                "ceten": Int64(all_prices["CETEN"]),
                "coutant": Int64(all_prices["Coutant"]),
                "externe": Int64(all_prices["Exté"]),
                "menu": Int64(all_prices["Menu"]),
                "privilegies": Int64(all_prices["Privilège"]),
                "staff_bar": Int64(all_prices["Staff"]),
                }
            }}
        collection_item.update_one(query, newvalues)
        Reappro["items"].append({
            "amount_of_bundle": Int64(nb_de_lots_acheter[i]),
            "amount_per_bundle": Int64(nb_produits_par_lots[i]),
            "bundle_cost_ht": prix_centimes,
            "item_id": item["id"],
            "item_name": item["name"],
            "item_picture_uri": item["picture_uri"],
            "tva": Int64(550),
            })
        Reappro["total_cost_ht"] += prix_centimes * int(nb_de_lots_acheter[i])
        Reappro["total_cost_ttc"] += prix_centimes * int(nb_de_lots_acheter[i]) * 1.055
    Reappro["total_cost_ht"] = Int64(Reappro["total_cost_ht"])
    Reappro["total_cost_ttc"] = Int64(Reappro["total_cost_ttc"])
    print(Reappro)
    collection_restocks.insert_one(Reappro)

if __name__ == '__main__':
    load_dotenv()
    client = MongoClient("mongodb://localhost:27017/")
    reappro_mongo(client, getenv("EMAIL"), "p")