from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import os
from dotenv import load_dotenv
load_dotenv()

mongodb_url = os.getenv('MONGODB_URL')
db_name = os.getenv('DB_NAME')
collection_name = os.getenv('COLLECTION_NAME')

class DatabaseManager:
    def __init__(self, db_name=db_name):
        try:
            self.client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
            self.client.server_info()
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print(f"Connected to MongoDB database: {db_name}, collection: {collection_name}")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
        except OperationFailure as e:
            print(f"MongoDB operation failed: {e}")

    def insert_tweet(self, tweet_data):
        if not self.db:
            print("No database connection.")
            return
        try:
            self.db.tweets.insert_one(tweet_data)
        except Exception as e:
            print(f"Error inserting tweet: {e}")

    def find_tweets_by_sentiment(self, sentiment):
        if not self.db:
            print("No database connection.")
            return None
        try:
            return self.db.tweets.find({"sentiment": sentiment})
        except Exception as e:
            print(f"Error finding tweets by sentiment: {e}")
            return []
        
    def find_all_tweets(self):
        if not self.db:
            print("No database connection.")
            return None
        try:
            return self.db.tweets.find()
        except Exception as e:
            print(f"Error finding all tweets: {e}")
            return []
        

database = DatabaseManager()

