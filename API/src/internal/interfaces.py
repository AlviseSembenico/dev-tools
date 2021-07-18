import os
import pymongo
from ..config import get_settings


settings = get_settings()

MONGO_CLIENT = pymongo.MongoClient(
    f"mongodb+srv://{settings.MONGO_DB_USER}:{settings.MONGO_DB_PASSWORD}@cluster0.lwysi.mongodb.net/{settings.MONGO_DB_NAME}?retryWrites=true&w=majority")
