import csv
from pathlib import Path

def csv_writer(file, data):
    """
    Write data to a CSV file path
    """
    with open(Path("csv") / file, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)

if __name__ == '__main__':
    data = [('Coca Cola', '31'), ('Coca Cherry', '30'), ('Coca Cola Zero', '60'), ('Fanta Orange', '35'), ('Lipton Peche', '27'), ('Oasis Tropical', '11'), ('Fanta Citron', '31'), ('Monster Energie', '34'), ('Oasis PCF', '8'), ('Orangina', '11'), ('Schweppes Agrume', '27'), ('Dr. Pepper', '18'), ('7up', '24'), ('Schweppes india tonic', '10'), ('Bonbons Haribo', '17'), ('Eau 50cL', '27'), ('Perrier Citron Vert', '21'), ('Monster Ultra Zero Sugar', '8'), ('Monster Ultra Paradise', '8'), ('Jus Orange', '4'), ('Jus fraise', '10'), ('Jus Multifruit', '4'), ('Jus Peche', '21'), ('Jus ACE', '18'), ('Jus Mangue', '1'), ('Jus Banane', '9'), ('7up mojito', '51'), ('Jus Pomme', '11'), ('Jus Raisin', '11'), ('Arizona PomeGranate', '8'), ('Jus Poire', '0'), ('Monster Ultra Gold', '8'), ('Arizona Mucho Mango', '4'), ('Arizona Green Tea', '0'), ('Arizona Lemon Tea', '3'), ('Fuzetea 33 CL', '26'), ('Jus Abricot', '20'), ('Dada Cerise', '0'), ('Volvic Fraise', '29'), ('Canada dry', '14'), ('Monster Mango Loco', '9'), ('Monster Pipeline Punch', '16'), ('Jus tomate', '8'), ('Arizona Pêche', '18'), ('Capri-Sun Multi Vitamin', '28'), ('7up Exotique', '15')]
    csv_writer('Inventaire.csv', data)