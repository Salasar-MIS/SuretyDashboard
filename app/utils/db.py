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

@st.cache_resource
def _get_client():
    """
    Single MongoClient shared across all Streamlit sessions.
    Pool tuned for a dashboard workload: many short reads, few writes.
    """
    return MongoClient(
        _get_uri(),
        maxPoolSize=20,
        minPoolSize=2,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=10000,
        retryWrites=True,
    )

def get_db():
    """Return the surety_dashboard database."""
    return _get_client()["surety_dashboard"]
