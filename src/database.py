import os
import certifi # Adicione esta importação
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        # Usamos o certifi para garantir que o SSL encontre a autoridade certificadora
        uri = os.getenv("MONGO_URI")
        self.client = MongoClient(uri, tlsCAFile=certifi.where()) 
        self.db = self.client.get_database("financa_pro")

    def get_collection(self, name):
        return self.db.get_collection(name)

db = Database()
