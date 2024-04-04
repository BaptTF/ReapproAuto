from pymongo import MongoClient
from datetime import datetime, timedelta
from datetime import timezone as tz
from dotenv import load_dotenv
from csvReader import csv_reader
from csvWriter import csv_writer
from os import getenv
from bson.int64 import Int64
import math

def arrondi_au_mutilple(x, a):
    if a <= 0:
        return x
    return math.ceil(x / a) * a

def calcul_optimal_amount(client, magasin, days=21, security=True):
    # Access a specific database
    db = client["bar"]

    # Access a specific collection within the database
    collection_transactions = db["transactions"]
    week_quantities = get_item_sales_weeks(collection_transactions, days)
    collection_items = db["items"]

    if magasin == "p":
        produits = csv_reader(file='Inventaire_Promocash.csv', row_number=0)
        nb_produits_par_lots = csv_reader(file='Inventaire_Promocash.csv', row_number=3)
    elif magasin == "a":
        produits = csv_reader(file='Inventaire_Auchan.csv', row_number=0)
        nb_produits_par_lots = csv_reader(file='Inventaire_Auchan.csv', row_number=3)
    else:
        print("Magasin inconnu")
        exit()
    update_optimal_amount = [('id', 'name', 'amount_sold', 'new_optimal_amount', 'old_optimal_amount')]
    update_optimal_manquant = [('id', 'name', 'amount_left', 'optimal_amount', 'optimal_amount')]
    print("La sécurité est désactivée, vous êtes sûr de ce que vous faites" if security == False else "La sécurité est activée, vous pouvez annuler à tout moment")
    for i in range(len(produits)):
        query = { "name": { "$regex": produits[i], "$options" :'i'}, "deleted_at": None}
        produit = collection_items.find_one(query)
        if produit["name"] in week_quantities.keys() and produit["amount_left"] != 0:
            new_optimal_amount = Int64(arrondi_au_mutilple(week_quantities[produit["name"]], int(nb_produits_par_lots[i]) // 2))
            if new_optimal_amount != produit["optimal_amount"]:
                update_optimal_amount.append((produit["_id"], produit["name"], week_quantities[produit["name"]], new_optimal_amount, produit["optimal_amount"]))
                if not security:
                    if input(f"Voulez vous modifier le montant optimal du produit {produit['name']} de {produit['optimal_amount']} pour {new_optimal_amount} (nb_produit_vendu: {int(week_quantities[produit['name']])})? (y/n)") == "y":
                        collection_items.update_one({"name": produit["name"]}, {"$set": {"optimal_amount": new_optimal_amount}})
                        print(f"{produit['name']} Modifier")
        else:
            update_optimal_manquant.append((produit["_id"], produit["name"], produit["amount_left"], produit["optimal_amount"], produit["optimal_amount"]))
    
    print("Modification écrite dans le fichier Update_optimal.csv et Update_optimal_manquant.csv")
    print("(id, name, amount_sold, new_optimal_amount, old_optimal_amount)")
    csv_writer('Update_optimal.csv', update_optimal_amount)
    csv_writer('Update_optimal_manquant.csv', update_optimal_manquant)

def get_item_sales_weeks(transactions_collection, w):
    # Calculate the date w weeks ago
    three_weeks_ago = int((datetime.now(tz.utc) - timedelta(days=w)).timestamp())
    # Create the pipeline for the aggregation
    pipeline = [
    {
        "$match": {
            "created_at": { "$gte": three_weeks_ago }
        }
    },
    {
        "$unwind": "$items"
    },
    {
        "$group": {
            "_id": "$items.item_id",
            "totalQuantity": { "$sum": "$items.item_amount" }
        }
    },
    {
        "$lookup": {
            "from": "items",
            "localField": "_id",
            "foreignField": "id",
            "as": "item_data"
        }
    },
    {
        "$unwind": "$item_data"
    },
    {
        "$project": {
            "_id": 0,
            "item_name": "$item_data.name",
            "totalQuantity": 1
        }
    },
    {
        "$group": {
            "_id": "$item_name",
            "totalQuantity": { "$sum": "$totalQuantity" }
        }
    }
]

    # Execute the aggregation and fetch the results
    results = transactions_collection.aggregate(pipeline)
    item_sales_dict = {result['_id']: result['totalQuantity'] for result in results}
    return item_sales_dict


if __name__ == '__main__':
    load_dotenv()
    client = MongoClient(f"mongodb://bar:{getenv('MONGO_MDP')}@mongo.telecomnancy.net:443/?authMechanism=DEFAULT&authSource=bar&directConnection=true&tls=true&tlsCertificateKeyFile={getenv('MONGO_PEM')}")
    calcul_optimal_amount(client, "p")
    #update_optimal_amount(client, "Update_optimal.csv")