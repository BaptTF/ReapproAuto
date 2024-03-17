from pymongo import MongoClient
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from os import getenv

load_dotenv()
client = MongoClient(f"mongodb://bar:{getenv('MONGO_MDP')}@mongo.telecomnancy.net:443/?authMechanism=DEFAULT&authSource=bar&directConnection=true&tls=true&tlsCertificateKeyFile={getenv('MONGO_PEM')}")

# Access a specific database
db = client["bar"]

# Access a specific collection within the database
collection = db["transactions"]

somme = 0
def get_quantity_sold(nom_produit):
    transactions = collection.find()
    by_day = defaultdict(int)
    by_week = defaultdict(int)
    for transaction in transactions:
        date = datetime.utcfromtimestamp(transaction["created_at"]).date()
        year, week, _ = date.isocalendar()
        if date not in by_day:
            by_day[date] = 0
        if (year, week) not in by_week:
            by_week[(year, week)] = 0
        if transaction["state"] == "finished":
            for item in transaction["items"]:
                if item["item_name"] == nom_produit:
                    by_day[date] += item["item_amount"]
                    by_week[(year, week)] += item["item_amount"]

    week_dates = sorted(by_week.keys())
    week_quantities = [by_week[date] for date in week_dates]
    dates = sorted(by_day.keys())
    dates_quantities = [by_day[date] for date in dates]
    return week_dates, week_quantities, dates, dates_quantities

def show_get_quantity_sold(nom_produit_liste):
    nom_produit_complet = ", ".join(nom_produit_liste)
    plt.figure(figsize=(10, 5))
    for i in range(len(nom_produit_liste)):
        nom_produit = nom_produit_liste[i]
        week_dates, week_quantities, dates, dates_quantities = get_quantity_sold(nom_produit)
        plt.plot(week_quantities, label=nom_produit)
    # test = [i for i in week_quantities_p1 if i != 0]
    # print(test)
    # moy = sum(week_quantities_p1)/len(week_quantities_p1)
    # moy_test = sum(test)/len(test)
    # print(moy, moy_test)
    plt.xticks(range(len(week_dates)), week_dates, rotation='vertical')
    plt.xlabel('Week (Year, Week number)')
    plt.ylabel('Quantity')
    plt.title(f'Quantity of {nom_produit_complet} sold per week')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    client.close()

def get_item_in_reappro(nom_produit):
    collection_restocks = client["bar"]["restocks"]
    reappro = collection_restocks.find()
    by_day = defaultdict(int)
    by_week = defaultdict(int)
    for r in reappro:
        date = datetime.utcfromtimestamp(r["created_at"]).date()
        year, week, _ = date.isocalendar()
        if date not in by_day:
            by_day[date] = 0
        if r["items"] == None:
            continue
        if (year, week) not in by_week:
            by_week[(year, week)] = 0
        for item in r["items"]:
            if item["item_name"] == nom_produit:
                by_day[date] += item["amount_of_bundle"] * item["amount_per_bundle"]
                by_week[(year, week)] += item["amount_of_bundle"] * item["amount_per_bundle"]

    week_dates = sorted(by_week.keys())
    week_quantities = [by_week[date] for date in week_dates]
    dates = sorted(by_day.keys())
    dates_quantities = [by_day[date] for date in dates]
    return week_dates, week_quantities, dates, dates_quantities

def show_get_item_in_reappro(nom_produit_liste):
    nom_produit_complet = ", ".join(nom_produit_liste)
    plt.figure(figsize=(10, 5))
    for i in range(len(nom_produit_liste)):
        nom_produit = nom_produit_liste[i]
        week_dates, week_quantities, dates, dates_quantities = get_item_in_reappro(nom_produit)
        plt.plot(week_quantities, label=nom_produit)
    plt.xticks(range(len(week_dates)), week_dates, rotation='vertical')
    plt.xlabel('Week (Year, Week number)')
    plt.ylabel('Quantity')
    plt.title(f'Quantity of {nom_produit_complet} in reappro per week')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    client.close()
    


if __name__ == "__main__":
    nom_produit_liste = ['Coca Cola', 'Coca Cola Zero','Coca Cherry', 'Oasis PCF', "Monster Energy", "Lipton Peche", "Oasis Tropical", "Kinder Bueno", "Orangina"]
    show_get_quantity_sold(nom_produit_liste)

#print(somme)
