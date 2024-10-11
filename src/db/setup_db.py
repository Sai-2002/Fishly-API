from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import gridfs

def setup():

    uri = "mongodb+srv://smnjr2002:smnjr2002@cluster0.efwsy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['fishie']
    fs = gridfs.GridFS(db)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return db, fs

db, fs = setup()
