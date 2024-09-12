from pymongo import MongoClient
from datetime import datetime, timedelta
from datetime import timezone as tz
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
        date = datetime.fromtimestamp(transaction["created_at"], tz.utc).date()
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

collection_restocks = db["restocks"]
def get_item_in_reappro(nom_produit):
    reappro = collection_restocks.find()
    by_day = defaultdict(int)
    by_week = defaultdict(int)
    for r in reappro:
        date = datetime.fromtimestamp(r["created_at"], tz.utc).date()
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
    
def get_amount_paid_per_person():
    transactions = collection.find()
    amount_paid_per_person = defaultdict(int)
    for transaction in transactions:
        if transaction["state"] == "finished":
            amount_paid = transaction["total_cost"]
            person = transaction["account_name"]
            if amount_paid < 10000:
                amount_paid_per_person[person] += amount_paid
    return amount_paid_per_person

def show_get_amount_paid_per_person():
    amount_paid_per_person = get_amount_paid_per_person()
    plt.figure(figsize=(20, 10))
    plt.bar(amount_paid_per_person.keys(), [i/100 for i in amount_paid_per_person.values()])
    plt.xticks(range(len(amount_paid_per_person.keys())), amount_paid_per_person.keys(), rotation="vertical")
    plt.xlabel('Person')
    plt.ylabel('Amount paid')
    plt.title('Amount paid per person')
    plt.grid(True)
    plt.tight_layout()
    plt.xlim(-0.5,len(amount_paid_per_person.keys())-.5)
    plt.show()
    client.close()

def show_get_amount_paid_for_one_person(person):
    amount_paid_per_person = get_amount_paid_per_person()
    print(person, amount_paid_per_person[person] / 100)

def get_amount_of_product_sold_for_last_2_week():
    transactions = collection.find()
    amount_of_product_sold = defaultdict(int)
    for transaction in transactions:
        date = datetime.fromtimestamp(transaction["created_at"], tz.utc).date()
        if transaction["state"] == "finished" and date > datetime.now().date() - timedelta(days=14) and transaction["total_cost"] > 0:
            for item in transaction["items"]:
                amount_of_product_sold[item["item_name"]] += item["item_amount"]
    sorted_amount_of_product_sold = dict(sorted(amount_of_product_sold.items(), key=lambda x: x[1], reverse=True))
    return sorted_amount_of_product_sold
    #return amount_of_product_sold

def show_get_amount_of_product_sold_for_last_2_week():
    amount_of_product_sold = get_amount_of_product_sold_for_last_2_week()
    plt.figure(figsize=(20, 10))
    #amount_of_product_sold["All Monster"] = amount_of_product_sold["Monster Energy"] + amount_of_product_sold["Monster Ultra Zero Sugar"] + amount_of_product_sold["Monster Ultra Paradise"] + amount_of_product_sold["Monster Ultra Gold"]+ amount_of_product_sold["Monster Mango Loco"] + amount_of_product_sold["Monster Zero Sucre"]
    print(len(amount_of_product_sold.keys()))
    plt.bar(amount_of_product_sold.keys(), amount_of_product_sold.values())
    plt.xticks(range(len(amount_of_product_sold.keys())), amount_of_product_sold.keys(), rotation='vertical')
    plt.xlabel('Product')
    plt.ylabel('Amount sold')
    plt.title('Amount of product sold for the last 2 weeks')
    plt.grid(True)
    plt.tight_layout()
    plt.xlim(-0.5,len(amount_of_product_sold.keys())-.5)
    plt.show()
    client.close()

collection_item = db["items"]
collection_category = db["categories"]
def create_list_of_product_in_category(category):
    category_id = collection_category.find_one({"name": category})["id"]
    items = collection_item.find({"category_id": category_id})
    return [item["name"] for item in items]

def get_amount_of_product_sold_for_last_2_week_per_category(category):
    transactions = collection.find()
    amount_of_product_sold = defaultdict(int)
    list_of_product_in_category = create_list_of_product_in_category(category)
    for transaction in transactions:
        date = datetime.fromtimestamp(transaction["created_at"], tz.utc).date()
        if transaction["state"] == "finished" and date > datetime.now().date() - timedelta(days=14) and transaction["total_cost"] > 0:
            for item in transaction["items"]:
                if item["item_name"] in list_of_product_in_category:
                    amount_of_product_sold[item["item_name"]] += item["item_amount"]
    sorted_amount_of_product_sold = dict(sorted(amount_of_product_sold.items(), key=lambda x: x[1], reverse=True))
    return sorted_amount_of_product_sold
    #return amount_of_product_sold

def show_get_amount_of_product_sold_for_last_2_week_per_category(category):
    amount_of_product_sold = get_amount_of_product_sold_for_last_2_week_per_category(category)
    plt.figure(figsize=(20, 10))
    #amount_of_product_sold["All Monster"] = amount_of_product_sold["Monster Energy"] + amount_of_product_sold["Monster Ultra Zero Sugar"] + amount_of_product_sold["Monster Ultra Paradise"] + amount_of_product_sold["Monster Ultra Gold"]+ amount_of_product_sold["Monster Mango Loco"] + amount_of_product_sold["Monster Zero Sucre"]
    print(len(amount_of_product_sold.keys()))
    plt.bar(amount_of_product_sold.keys(), amount_of_product_sold.values())
    plt.xticks(range(len(amount_of_product_sold.keys())), amount_of_product_sold.keys(), rotation='vertical')
    plt.xlabel('Product')
    plt.ylabel('Amount sold')
    plt.title('Amount of product sold for the last 2 weeks')
    plt.grid(True)
    plt.tight_layout()
    plt.xlim(-0.5,len(amount_of_product_sold.keys())-.5)
    plt.show()
    client.close()

from csvReader import csv_reader
def get_amount_of_product_sold_for_last_2_week_per_inventory(filename):
    transactions = collection.find()
    amount_of_product_sold = defaultdict(int)
    list_of_product_in_inventory = csv_reader(filename, 0)
    for transaction in transactions:
        date = datetime.fromtimestamp(transaction["created_at"], tz.utc).date()
        if transaction["state"] == "finished" and date > datetime.now().date() - timedelta(days=14) and transaction["total_cost"] > 0:
            for item in transaction["items"]:
                if item["item_name"] in list_of_product_in_inventory:
                    amount_of_product_sold[item["item_name"]] += item["item_amount"]
    sorted_amount_of_product_sold = dict(sorted(amount_of_product_sold.items(), key=lambda x: x[1], reverse=True))
    return sorted_amount_of_product_sold

def show_get_amount_of_product_sold_for_last_2_week_per_inventory(filename):
    amount_of_product_sold = get_amount_of_product_sold_for_last_2_week_per_inventory(filename)
    plt.figure(figsize=(20, 10))
    #amount_of_product_sold["All Monster"] = amount_of_product_sold["Monster Energy"] + amount_of_product_sold["Monster Ultra Zero Sugar"] + amount_of_product_sold["Monster Ultra Paradise"] + amount_of_product_sold["Monster Ultra Gold"]+ amount_of_product_sold["Monster Mango Loco"] + amount_of_product_sold["Monster Zero Sucre"]
    print(len(amount_of_product_sold.keys()))
    plt.bar(amount_of_product_sold.keys(), amount_of_product_sold.values())
    plt.xticks(range(len(amount_of_product_sold.keys())), amount_of_product_sold.keys(), rotation='vertical')
    plt.xlabel('Product')
    plt.ylabel('Amount sold')
    plt.title('Amount of product sold for the last 2 weeks')
    plt.grid(True)
    plt.tight_layout()
    plt.xlim(-0.5,len(amount_of_product_sold.keys())-.5)
    plt.show()
    client.close()

def get_the_time_of_last_transaction_for_each_day_per_product(produit, nb_jours=14):
    transactions = collection.find()
    last_transaction_time_per_day_per_product = defaultdict(lambda: datetime.min.replace(tzinfo=tz.utc))
    for transaction in transactions:
        date = datetime.fromtimestamp(transaction["created_at"], tz=tz.utc).date()
        if transaction["state"] == "finished" and date > datetime.now().date() - timedelta(days=nb_jours) and transaction["total_cost"] > 0:
            for item in transaction["items"]:
                if item["item_name"] == produit:
                    if datetime.fromtimestamp(transaction["created_at"], tz=tz.utc) > last_transaction_time_per_day_per_product[date]:
                        last_transaction_time_per_day_per_product[date] = datetime.fromtimestamp(transaction["created_at"], tz=tz.utc)
    return last_transaction_time_per_day_per_product

def get_the_time_of_last_reappro_for_each_day_per_product(produit, nb_jours=14):
    reappro = collection_restocks.find()
    last_reappro_time_per_day_per_product = defaultdict(lambda: datetime.min.replace(tzinfo=tz.utc))
    for r in reappro:
        date = datetime.fromtimestamp(r["created_at"], tz=tz.utc).date()
        if r["items"] == None:
            continue
        if date > datetime.now().date() - timedelta(days=nb_jours):
            for item in r["items"]:
                if item["item_name"] == produit:
                    if datetime.fromtimestamp(r["created_at"], tz=tz.utc) > last_reappro_time_per_day_per_product[date]:
                        last_reappro_time_per_day_per_product[date] = datetime.fromtimestamp(r["created_at"], tz=tz.utc)
    return last_reappro_time_per_day_per_product
    
def addlabels(x,y,label):
    for i in range(len(x)):
        plt.text(i, y[i], label[i], ha = 'center')

import calendar
def show_the_time_of_last_transaction_for_each_day_per_product(produit, nb_jours=14):
    last_transaction_time_per_day_per_product = get_the_time_of_last_transaction_for_each_day_per_product(produit, nb_jours)
    last_reappro_time_per_day_per_product = get_the_time_of_last_reappro_for_each_day_per_product(produit, nb_jours)
    print(len(last_transaction_time_per_day_per_product.values()), len(last_reappro_time_per_day_per_product.values()))
    #print(last_reappro_time_per_day_per_product)
    plt.figure(figsize=(20, 10))
    label = [str(value.astimezone().time()) for value in last_transaction_time_per_day_per_product.values()]
    value = []
    for date in last_transaction_time_per_day_per_product.keys():
        minute = (last_transaction_time_per_day_per_product[date] - last_reappro_time_per_day_per_product[date]).total_seconds() // 60
        if minute > 3600*12 or minute < 0:
            minute = 0
        value.append(minute)
    #value = [(i - j).total_seconds() // 60 for i,j in zip(last_transaction_time_per_day_per_product.values(), last_reappro_time_per_day_per_product.values())]
    display = [(calendar.day_name[i.weekday()] + " " + str(i)) for i in last_transaction_time_per_day_per_product.keys()]
    plt.bar(display, value)
    addlabels(display, value, label)
    plt.xticks(range(len(last_transaction_time_per_day_per_product.keys())), display, rotation='vertical')
    plt.xlabel('Day')
    plt.ylabel('Time between the reappro and the last transaction (minutes)')
    plt.title(f'Time of last transaction of {produit} for the last 2 weeks per day (minutes)') 
    plt.grid(True)
    plt.tight_layout()
    plt.xlim(-0.5,len(last_transaction_time_per_day_per_product.keys())-.5)
    plt.show()
    client.close()

def get_amount_of_drinks_for_last_year(list_of_item):
    transactions = collection.find()
    dictio = {}
    for transaction in transactions:
        if transaction["total_cost"] > 0:
            for item in transaction["items"]:
                for item_search in list_of_item:
                    if item_search in item["item_name"]:
                        if item["item_name"] in dictio:
                            dictio[item["item_name"]] += item["item_amount"]
                        else:
                            dictio[item["item_name"]] = item["item_amount"]
    return dictio



if __name__ == "__main__":
    nom_produit_liste = ['Coca Cola', 'Coca Cola Zero','Coca Cherry', 'Oasis PCF', "Monster Energy", "Lipton Peche", "Oasis Tropical", "Kinder Bueno", "Orangina"]
    #nom_produit_test = ["Jus Raisin"]
    #show_get_quantity_sold(nom_produit_liste)
    #show_get_amount_paid_per_person()
    #show_get_amount_paid_for_one_person("Aristide URLI")
    #show_get_amount_of_product_sold_for_last_2_week()
    #show_get_amount_of_product_sold_for_last_2_week_per_category("Viennoiseries")
    #show_get_amount_of_product_sold_for_last_2_week_per_inventory("Inventaire_Promocash.csv")
    #show_the_time_of_last_transaction_for_each_day_per_product("Pain au Chocolat(ine)", 30)
    #print(get_amount_of_drinks_for_last_year(["Monster"]))

#print(somme)
