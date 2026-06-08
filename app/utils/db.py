import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

_client = None

def _get_uri() -> str:
    """
    Resolve MongoDB URI.
    Streamlit Cloud stores secrets in st.secrets; local dev uses .env.
    """
    # Try Streamlit secrets first (Streamlit Cloud deployment)
    try:
        import streamlit as st
        return st.secrets["MONGO_URI"]
    except (ImportError, KeyError):
        pass
    # Fall back to .env / environment variable (local dev)
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise EnvironmentError("MONGO_URI not set — add it to .env or Streamlit secrets.")
    return uri

def get_db():
    """Return the surety_dashboard database, reusing the connection."""
    global _client
    if _client is None:
        _client = MongoClient(_get_uri(), serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
    db_name = os.getenv("MONGO_DB", "surety_dashboard")
    return _client[db_name]
