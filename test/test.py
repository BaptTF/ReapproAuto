import ReapproAuto
import ReapproAuto.Auchan
import ReapproAuto.inventaireMongo
import ReapproAuto.Promocash
import ReapproAuto.Reappro
import ReapproAuto.ReapproMongo
import ReapproAuto.remiseStockManuelle
import ReapproAuto.UpdatePricePromocash
import ReapproAuto.PrintCalculPrixTotal
import ReapproAuto.CalculOptimalAmount
import ReapproAuto.UpdateOptimalAmount
import ReapproAuto.Install
from pymongo import MongoClient
from os import getenv
import dotenv

if __name__ == '__main__':
    dotenv.load_dotenv(override=True)
    client = MongoClient(f"mongodb://bar:{getenv('MONGO_MDP')}@mongo.telecomnancy.net:443/?authMechanism=DEFAULT&authSource=bar&directConnection=true&tls=true&tlsCertificateKeyFile={getenv('MONGO_PEM')}")
    ReapproAuto.inventaireMongo.inventaire_mongo(client, "Inventaire_Promocash.csv")