import os
from pymongo import MongoClient
import dotenv
class Database:
    def __init__(self):
        dotenv.load_dotenv()
        self.uri = os.getenv("MONGO_URI")
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.db = self.client['financa_inteligente_db']
            # Teste rápido
            self.client.server_info()
            print(f"✅ Conectado ao MongoDB: {self.uri}")
        except Exception as e:
            print(f"❌ Erro Crítico no Mongo: {e}")
            self.db = None

    def get_collection(self, collection_name):
        if self.db is not None:
            return self.db[collection_name]
        return None

db = Database()