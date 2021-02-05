from flask import jsonify
import json
import random
import bcrypt
from datetime import datetime

from pymongo import MongoClient
client = MongoClient("mongodb+srv://Admin:kdjhi832h!ya6@cluster0.l6quu.mongodb.net/hackaton?retryWrites=true&w=majority")
db = client.MafiaGoDB
users = db.users
codes = db.codes

from modules import hf

class request_precessing():

    def __init__(self):
        pass

    def reg_code(self, data):
        data = dict(json.loads(data))
        user = users.find_one({
            "email": data['email']
        })
        if user != None:
            return jsonify("incorrect_email")
        user = codes.find_one({
            "email": data['email']
        })
        if user != None:
            code = random.randrange(10**6, 10**7, 1)
            codes.update_one(
                {"email": data['email']},
                {"$set":
                     {"code": code, "time": datetime.utcnow()}
                }
            )
            hf.send_email('Подтверждение регистрации', data['email'], 'Ваш код подтверждения: %s, он будет действителен в течение часа. Если это не Вы, то просто проигнорируйте данное письмо' % (code))
            return jsonify("send_code")
        else:
            code = random.randrange(10 ** 6, 10 ** 7, 1)
            codes.insert_one({
                "email": data['email'],
                "code": code,
                "time": datetime.utcnow(),
            })
            hf.send_email('Подтверждение регистрации', data['email'], 'Ваш код подтверждения: %s, он будет действителен в течение часа. Если это не Вы, то просто проигнорируйте данное письмо' % (code))
            return jsonify("send_code")

    def reg_in(self, data):
        data = dict(json.loads(data))
        user = users.find_one({
            "email": data['email']
        })
        if user != None:
            return jsonify("incorrect_email")
        else:
            user = codes.find_one({
                "email": data['email']
            })
            if (datetime.utcnow() - user['time']).seconds > 3600:
                codes.delete_one({
                    "email": data['email']
                })
                return jsonify('code_time_out')
            elif user['code'] == data['code']:
                users.insert_one({
                    "email": data['email'],
                    "password": bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt(16)),
                    "avatar": '',
                    "role": 'user',
                    "user_id": self.make_user_id(),
                    "session_id": bcrypt.hashpw(self.make_session_id().encode(), bcrypt.gensalt(16)),
                    "chats": {},
                    "banned": False,
                    "ban_time": [],
                    "ban_reason": '',
                })
                codes.delete_one({
                    "email": data['email']
                })
                return jsonify("reg_in")
            else:
                return jsonify("incorrect_code")

    def log_in(self, data):
        data = dict(json.loads(data))
        user = users.find_one({
            "email": data['email']
        })
        if user == None:
            return jsonify("incorrect_email")
        elif not bcrypt.checkpw(data['password'].encode(), user['password']):
            return jsonify("incorrect_password")
        else:
            session_id = self.make_session_id()
            users.update_one(
                {"email": data['email']},
                {"$set":
                     {"session_id": bcrypt.hashpw(session_id.encode(), bcrypt.gensalt(16))}
                 }
            )
            del user['_id']
            del user['password']
            del user['banned']
            del user['ban_time']
            del user['ban_reason']
            user['session_id'] = session_id
            return jsonify(user)

    def get_information(self, data):
        data = dict(json.loads(data))
        if not hf.check_session_id(data): return '310'
        else:
            user = users.find_one({
                "email": data['email']
            })
            del user['_id']
            del user['password']
            del user['banned']
            del user['ban_time']
            del user['ban_reason']
            del user['session_id']
            return jsonify(user)

    def make_user_id(self):
        user = {}
        while user != None:
            result = ''
            letters = '0123456789qwertyuiopasdfghjklzxcvbnm'
            maximum = len(letters)
            for i in range(16):
                result += letters[random.randrange(0, maximum, 1)]
            user = users.find_one({
                "user_id": result
            })
        return result

    def make_session_id(self):
        user = {}
        while user != None:
            result = ''
            letters = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
            maximum = len(letters)
            for i in range(256):
                result += letters[random.randrange(0, maximum, 1)]
            user = users.find_one({
                "session_id": result
            })
        return result

rp = request_precessing()