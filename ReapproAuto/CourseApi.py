import requests
import json
from ReapproAuto.csvWriter import csv_writer

def course(card_id: str, card_pin: str, fournisseur: str):
    # Make the POST request to /auth/card
    url = 'https://bar.telecomnancy.net/auth/card'
    headers = {'X-Local-Token': 'jesuisleplusfort', 'Content-Type': 'application/json'}
    data = {'card_id': card_id, 'card_pin': card_pin}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Make the GET request to /course
    url = 'https://bar.telecomnancy.net/course'
    params = {'fournisseur': fournisseur}
    response = requests.get(url, cookies=response.cookies.get_dict(), params=params)

    # Print the response
    if response.status_code != 200:
        print("Mauvais Code PIN ou Card ID")
    else:
        CourseTab = [('Produit', 'Nombre de lots à acheter', 'Nombre de produits', 'Nombre de produits supposé', 'Nombre de produits par lots', 'REF')]
        CourseNonDrive = [('Produit', 'Nombre de lots à acheter', 'Nombre de produits', 'Nombre de produits supposé', 'Nombre de produits par lots')]
        course = response.json()
        for row in course["items"]:
            item = row["item"]
            if "ref_bundle" in item:
                CourseTab.append((item["name"], row["amountToBuy"], item["amount_left"], item["optimal_amount"], item["amount_per_bundle"], item["ref_bundle"]))
            else:
                CourseNonDrive.append((item["name"], row["amountToBuy"], item["amount_left"], item["optimal_amount"], item["amount_per_bundle"]))
    csv_writer("Course.csv", CourseTab)
    csv_writer("Course_non_drive.csv", CourseNonDrive)
if __name__ == "__main__":
    course("0", "1234", "promocash")