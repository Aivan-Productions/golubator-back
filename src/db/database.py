from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings


logger.add("logs/debug.json", format="{time} {level} {message}", level="DEBUG", serialize=True)

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        uri = f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@mongo:27017"
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[settings.MONGO_DB_NAME]
        logger.info("Connected to mongodb")

    async def close(self):
        if self.client:
            self.client.close()
        logger.info("Disconected to mongodb")

    def get_collection(self, collection_name: str):
        if self.db is not None:
            return self.db[collection_name]
        else:
            logger.warning("Data not connected")
            raise Exception("Database not connected")


mongodb = MongoDB()
