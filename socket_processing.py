from flask_socketio import emit
from datetime import datetime

from pymongo import MongoClient
client = MongoClient("mongodb+srv://Admin:kdjhi832h!ya6@cluster0.l6quu.mongodb.net/hackaton?retryWrites=true&w=majority")
db = client.MafiaGoDB
collection = db.collection

class socket_processing():

    def __init__(self):
        pass

sp = socket_processing()