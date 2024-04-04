from pymongo import MongoClient
from datetime import timezone as tz
from dotenv import load_dotenv
from csvReader import csv_reader
from os import getenv
from bson.int64 import Int64
from bson.objectid import ObjectId

def update_optimal_amount(client, file, security=True):
    db = client["bar"]
    collection_items = db["items"]
    try:
        id = csv_reader(file, row_number=0)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file}, Erreur: {e}")
        exit()
    produits = csv_reader(file, row_number=1)
    amount_sold = csv_reader(file, row_number=2)
    optimal_amount = csv_reader(file, row_number=3)
    old_optimal_amount = csv_reader(file, row_number=4)
    print("La sécurité est désactivée, vous êtes sûr de ce que vous faites" if security == False else "La sécurité est activée, vous pouvez annuler à tout moment")
    for row in range(len(id)):
        if not security:
            ans = input(f"Voulez vous modifier le montant optimal du produit {produits[row]} de {old_optimal_amount[row]} pour {optimal_amount[row]} (nb_produit_vendu: {amount_sold[row]})? (y/n/exit) ")
            if ans == "y":
                collection_items.update_one({"_id": ObjectId(id[row])}, {"$set": {"optimal_amount": Int64(optimal_amount[row])}})
            elif ans == "n":
                print(f"Modification de {produits[row]} annulé")
            else:
                print("Modification annulé")
                exit()
        else:
            print(f"Voulez vous modifier le montant optimal de {produits[row]} pour {optimal_amount[row]} (nb_produit_vendu: {amount_sold[row]})")
    
if __name__ == '__main__':
    load_dotenv()
    client = MongoClient("mongodb://localhost:27017/")
    update_optimal_amount(client, 'Update_optimal.csv', security=False)