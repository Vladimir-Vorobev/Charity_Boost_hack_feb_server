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
            user['projects']['now'][data['num']]['chats'].append({'business': data['business'], 'user_id': data['user_id']})
            users.find_and_modify(query={"user_id": data['user_f_id']}, update={"$set": {"projects": user['projects']}})
        emit('create_chat', {'user_f_id': data['user_f_id'], 'num': data['num']})

    def get_chat(self, data):
        if not hf.check_session_id(data): return
        chat = chat_fund.find_one({
            'user_id': data['user_id'],
            'user_f_id': data['user_f_id'],
            'num': data['num'],
        })
        del chat['_id']
        emit('get_chat', chat)

    def send_message(self, data):
        if not hf.check_session_id(data): return
        chat = chat_fund.find_one({
            'user_id': data['user_id'],
            'user_f_id': data['user_f_id'],
            'num': data['num'],
        })
        mes = {'mes': data['mes'], 'from': data['from'], 'id': len(chat['messages']), 'time': datetime.utcnow().isoformat(), 'is_readed': False}
        chat['messages'].append(mes)
        chat_fund.find_and_modify(query={'user_id': data['user_id'], 'user_f_id': data['user_f_id'], 'num': data['num']}, update={"$set": {"messages": chat['messages']}})
        fund_sid = users.find_one({
            'user_id': data['user_f_id'],
        })
        business_sid = users.find_one({
            'user_id': data['user_id'],
        })
        emit('new_message', mes, room=fund_sid['sid'])
        emit('new_message', mes, room=business_sid['sid'])

    def read_message(self, data):
        if not hf.check_session_id(data): return

    def delete_chat(self, data):
        if not hf.check_session_id(data): return

    def new_sid(self, data):
        if not hf.check_session_id(data): return
        users.find_and_modify(query={"email": data['email']}, update={"$set": {"sid": data['sid']}})

sp = socket_processing()