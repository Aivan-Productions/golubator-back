from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        uri = f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@localhost:27017"
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[settings.MONGO_DB_NAME]
        print("Connected to MongoDB")

    async def close(self):
        """Закрытие соединения с MongoDB."""
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")

    def get_collection(self, collection_name: str):
        """Получить коллекцию из базы данных."""
        if self.db is not None:
            return self.db[collection_name]
        else:
            raise Exception("Database not connected")

# Создаем экземпляр класса для использования в приложении
mongodb = MongoDB()
