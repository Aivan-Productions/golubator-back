from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_INITDB_ROOT_USERNAME=os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD=os.getenv("MONGO_INITDB_ROOT_PASSWORD")


url = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@localhost:27017"
client = MongoClient(url)
db = client['mydb']

collection_messages = db['messages']
collection_emojis = db['emojis']

def insert_message(message_data: dict):
    result = collection_messages.insert_one(message_data)
    return result.inserted_id


def get_all_messages():
    data = collection_messages.find()
    res = []
    for doc in data:
        res.append({
            'text': doc['text'],
            'emoji': doc['emoji'],
            'timestamp': doc['timestamp'],
        })
    return res


def get_emoji():
    data = collection_emojis.find_one()
    if data:
        return data['emoji']
    else:
        return None

def remove_emoji(emoji):
    collection_emojis.delete_one({'emoji': emoji})
