import requests
import json
from ReapproAuto.csvReader import csv_reader

def reapproApi(card_id: str, card_pin: str, magasin: str):
    # Récupération des prix
    produits = csv_reader(file='Prix.csv', row_number=0)
    nb_de_lots_acheter = csv_reader(file='Prix.csv', row_number=1)
    nb_produits_par_lots = csv_reader(file='Prix.csv', row_number=2)
    prix = csv_reader(file='Prix.csv', row_number=3)
    id_produits = csv_reader(file='Prix.csv', row_number=5)
    tva_produits = csv_reader(file='Prix.csv', row_number=6)

    if magasin == "p":
        fournisseur = "promocash"
    else:
        fournisseur = "auchan_drive"

    # Make the POST request to /auth/card
    url = 'https://bar.telecomnancy.net/api/auth/card'
    headers = {'X-Local-Token': 'ceciestuneborne', 'Content-Type': 'application/json'}
    data = {'card_id': card_id, 'card_pin': card_pin}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    cookies = response.cookies.get_dict()

    NewRestock = {
        "items": [],
        "total_cost_ht": 0,
        "total_cost_ttc": 0,
        "type": fournisseur,
    }
    for row in range(len(produits)):
        if magasin == "p":
            prixHT = int(float(prix[row]) * 100)
            prixTTC = int(float(prix[row]) * 100 * (1 + (int(tva_produits[row]) / 10000)))
        else:
            prixHT = int(float(prix[row]) * 100 / (1 + (int(tva_produits[row]) / 10000)))
            prixTTC = int(float(prix[row]) * 100)
        NewRestock["total_cost_ht"] += prixHT
        NewRestock["total_cost_ttc"] += prixTTC
        NewRestockItem = {
            "item_id": id_produits[row],
            "amount_of_bundle": int(nb_de_lots_acheter[row]),
            "amount_per_bundle": int(nb_produits_par_lots[row]),
            "bundle_cost_ht": prixHT,
            "bundle_cost_ttc": prixTTC,
            "tva": int(tva_produits[row]),   
        }
        NewRestock["items"].append(NewRestockItem)
    print(NewRestock)

    url = 'https://bar.telecomnancy.net/api/restocks'
    headers = {'X-Local-Token': 'ceciestuneborne', 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(NewRestock), cookies=cookies)
    if response.status_code == 201:
        print("Reappro réalisé avec succès")
    else:
        print("Il y a eu un problème avec la Réappro, essayez sur le site du bar directement")

if __name__ == "__main__":
    reapproApi("0", "1234", "p")
