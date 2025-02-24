from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_INITDB_ROOT_USERNAME=os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD=os.getenv("MONGO_INITDB_ROOT_PASSWORD")


# available emojis
emojis = {'🤢', '😍', '👽', '🥸', '🥳', '🐵'}
data = {}

url = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@localhost:27017"
client = MongoClient(url)
db = client['mydb']
collection = db['messages']

def insert_message(message_data: dict):
    result = collection.insert_one(message_data)
    return result.inserted_id


def get_all_messages():
    data = collection.find()
    res = []
    for doc in data:
        res.append({
            'text': doc['text'],
            'emoji': doc['emoji'],
            'timestamp': doc['timestamp'],
        })
    return res
