from pymongo import MongoClient
from csvReader import csv_reader
from csvWriter import csv_writer
from os import getenv
from dotenv import load_dotenv

# Create a MongoClient object and specify the connection URL
def inventaire_mongo(client, file):
    # Access a specific database
    db = client["bar"]
    # Access a specific collection within the database
    collection = db["items"]

    # Perform operations on the collection
    # For example, you can insert a document
    # Retrieve all documents from the collection

    produits = csv_reader(file, row_number=0)
    supposed_nb_produits = csv_reader(file, row_number=2)
    nb_produits_par_lots = csv_reader(file, row_number=3)
    ifls_produits_promocash = csv_reader(file, row_number=4)

    Inventaire = []

    for i in range(len(produits)):
        query = { "name": { "$regex": produits[i], "$options" :'i' }}
        produit = collection.find_one(query)
        if produit == None:
            amount_left = "Produit non trouvé"
            optimal_amount = supposed_nb_produits[i]
        else:
            amount_left = produit["amount_left"]
            optimal_amount = produit["optimal_amount"]
        Inventaire.append((produits[i], amount_left, optimal_amount, nb_produits_par_lots[i], ifls_produits_promocash[i]))

    csv_writer(file, Inventaire)

if __name__ == '__main__':
    load_dotenv()
    client = MongoClient(f"mongodb://bar:{getenv('MONGO_MDP')}@mongo.telecomnancy.net:443/?authMechanism=DEFAULT&authSource=bar&directConnection=true&tls=true&tlsCertificateKeyFile={getenv('MONGO_PEM')}")
    inventaire_mongo(client)