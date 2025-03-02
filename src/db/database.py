from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        uri = f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@mongo:27017"
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[settings.MONGO_DB_NAME]
        print("Connected to MongoDB")

    async def close(self):
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")

    def get_collection(self, collection_name: str):
        if self.db is not None:
            return self.db[collection_name]
        else:
            raise Exception("Database not connected")


mongodb = MongoDB()
