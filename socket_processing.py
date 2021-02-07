from flask_socketio import emit
from datetime import datetime
import json

from modules import hf

from pymongo import MongoClient
client = MongoClient("mongodb+srv://Admin:kdjhi832h!ya6@cluster0.l6quu.mongodb.net/hackaton?retryWrites=true&w=majority")
db = client.hackaton
chat_fund = db.chat_fund
users = db.users

class socket_processing():

    def __init__(self):
        pass

    def create_chat(self, data):
        if not hf.check_session_id(data): return
        chat = chat_fund.find_one({
            'user_id': data['user_id'],
            'user_f_id': data['user_f_id'],
            'num': data['num'],
        })
        if chat == None:
            chat_fund.insert_one({
                'user_id': data['user_id'],
                'user_f_id': data['user_f_id'],
                'num': data['num'],
                'fund': data['fund'],
                'business': data['business'],
                'messages': [],
            })
            user = users.find_one({
                {"user_id": data['user_f_id']},
            })
            user['chats'].append({'business': data['business'], 'user_id': data['iser_id']})
            users.update_one({
                {"user_id": data['user_f_id']},
                {"$set":
                     {"chats": user['chats']}
                 }
            })
        emit('create_chat', {'user_f_id': data['user_f_id'], 'num': data['num']})

    def get_chat(self, data):
        if not hf.check_session_id(data): return
        chat = chat_fund.find_one({
            'user_id': data['user_id'],
            'user_f_id': data['user_f_id'],
            'num': data['num'],
        })
        del chat['_id']
        emit(chat)

    def send_message(self, data):
        if not hf.check_session_id(data): return

    def read_message(self, data):
        if not hf.check_session_id(data): return

    def delete_chat(self, data):
        if not hf.check_session_id(data): return

sp = socket_processing()