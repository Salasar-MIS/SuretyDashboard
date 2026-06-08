import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

_client = None

def get_db():
    """Return the surety_dashboard database, reusing the connection."""
    global _client
    if _client is None:
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise EnvironmentError("MONGO_URI not set in .env")
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Verify connectivity on first use
        _client.admin.command("ping")
    db_name = os.getenv("MONGO_DB", "surety_dashboard")
    return _client[db_name]
