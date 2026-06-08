import os
from dotenv import load_dotenv
from pymongo import MongoClient
import streamlit as st

load_dotenv()

def _get_uri() -> str:
    """Resolve MongoDB URI — Streamlit secrets first, .env fallback."""
    try:
        return st.secrets["MONGO_URI"]
    except (AttributeError, KeyError):
        pass
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise EnvironmentError("MONGO_URI not set — add it to .env or Streamlit secrets.")
    return uri

# Cache the MongoClient across all Streamlit sessions (recommended pattern)
@st.cache_resource
def _get_client():
    client = MongoClient(_get_uri(), serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    return client

def get_db():
    """Return the surety_dashboard database."""
    return _get_client()["surety_dashboard"]
