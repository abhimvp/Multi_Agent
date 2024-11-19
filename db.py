from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

# connect to the AstraDB database
# Go to AstraDB database -> Connection Details -> copy the endpoint and store that in env
ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")


# define a function to connect to the client
@st.cache_resource  # everytime we call this function we return the same reference , the same database object rather than reconnecting to this database tonnes of times
def get_db():
    client = DataAPIClient(TOKEN)
    db = client.get_database_by_api_endpoint(ENDPOINT)
    return db

db = get_db()
# idea here is to define different collections that i might want to connect to , 
# & create these collections if they don't already exist
collection_names = ["personal_data","notes"]

for collection_name in collection_names:
    try:
        db.create_collection(collection_name)
    except:
        pass
        
personal_data_collection = db.get_collection("personal_data")
notes_collection = db.get_collection("notes")