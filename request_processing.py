from flask import jsonify
import json
import random
import bcrypt
from datetime import datetime

from pymongo import MongoClient
client = MongoClient("mongodb+srv://Admin:kdjhi832h!ya6@cluster0.l6quu.mongodb.net/hackaton?retryWrites=true&w=majority")
db = client.hackaton
users = db.users
codes = db.codes
projects = db.projects

cities = {}

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
            elif user['code'] == int(data['code']):
                if data['role'] == 'fund':
                    users.insert_one({
                        "name": data['name'],
                        "number": data['number'],
                        "certificate": data['certificate'],
                        "phone": data['phone'],
                        "address": data['address'],
                        "site": data['site'],
                        "email": data['email'],
                        "password": bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt(16)),
                        "avatar": '',
                        "role": 'fund',
                        "user_id": self.make_user_id(),
                        "session_id": bcrypt.hashpw(self.make_session_id().encode(), bcrypt.gensalt(16)),
                        "projects": {'now': {}, 'archive': {}},
                        "banned": False,
                        "ban_time": [],
                        "ban_reason": '',
                    })
                    codes.delete_one({
                        "email": data['email']
                    })
                    return jsonify("reg_in")

                elif data['role'] == 'business':
                    users.insert_one({
                        "name": data['name'],
                        "full_name_responsible_person": data['full_name_responsible_person'],
                        "phone": data['phone'],
                        "email": data['email'],
                        "password": bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt(16)),
                        "avatar": '',
                        "role": 'business',
                        "user_id": self.make_user_id(),
                        "session_id": bcrypt.hashpw(self.make_session_id().encode(), bcrypt.gensalt(16)),
                        "projects": {},
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

    def add_project(self, data):
        data = dict(json.loads(data))
        if not hf.check_session_id(data): return '310'
        else:
            user = users.find_one({
                "email": data['email']
            })
            if user['role'] != 'fund': return 310
            else:
                id = self.make_session_id()
                user['projects']['now'][id] = {
                    'num': id,
                    'category': data['category'],
                    'type_help': data['type_help'],
                    'image': data['image'],
                    'city': data['city'],
                    'title': data['title'],
                    'help': data['help'],
                    'money': data['money'],
                    'helpers': [],
                }
                users.update_one(
                    {"email": data['email']},
                    {"$set":
                         {"projects": user['projects']}
                     }
                )
                projects.insert_one({
                    'author': data['email'],
                    'num': id,
                    'category': data['category'],
                    'type_help': data['type_help'],
                    'image': data['image'],
                    'city': data['city'],
                    'title': data['title'],
                    'help': data['help'],
                    'money': data['money'],
                })
                if data['city'] not in cities:
                    cities[data['city']] = 1
                else:
                    cities[data['city']] += 1
                return jsonify('OK')

    def get_projects(self, data):
        data = dict(json.loads(data))
        res = []
        for project in projects.find(data):
            del project['_id']
            res.append(project)
        res_cities = ['Все города']
        for city in cities:
            if city != 'Все города': res_cities.append(city)
        return jsonify([res, res_cities])

    def get_my_now_projects(self, data):
        data = dict(json.loads(data))
        if not hf.check_session_id(data): return '310'
        else:
            res = []
            user = users.find_one({
                "email": data['email']
            })
            if user['role'] == 'fund':
                for project in user['projects']['now']:
                    res.append(user['projects']['now'][project])
            return jsonify(res)

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

    def reload_cities(self):
        for city in projects.find():
            if city['city'] not in cities:
                cities[city['city']] = 1
            else:
                cities[city['city']] += 1

rp = request_precessing()