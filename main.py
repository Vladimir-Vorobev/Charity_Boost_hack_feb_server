from flask import Flask, make_response, request, session, copy_current_request_context
import threading
from server import app, sio

from socket_processing import sp
from request_processing import rp
from modules import hf

@app.route('/', methods = ['GET','POST'])
def code():
    return "Все работает"

@app.route('/reg-code/', methods = ['POST'])
def reg_code():
    return rp.reg_code(request.data)

@app.route('/registration/', methods = ['POST'])
def reg_in():
    return rp.reg_in(request.data)

@app.route('/login/', methods = ['POST'])
def log_in():
    return rp.log_in(request.data)

@app.route('/get_information/', methods = ['POST'])
def get_information():
    return rp.get_information(request.data)

@app.route('/add_project/', methods = ['POST'])
def add_project():
    return rp.add_project(request.data)

@app.route('/get_projects/', methods = ['POST'])
def get_projects():
    return rp.get_projects(request.data)

@app.route('/get_my_now_projects/', methods = ['POST'])
def get_my_now_projects():
    return rp.get_my_now_projects(request.data)

@app.route('/connect_with_admin/', methods = ['POST'])
def connect_with_admin():
    return rp.connect_with_admin(request.data)

# @app.route('/user/<id>/')
# def user_profile(id):
#     return rp.user_profile(id)

@sio.on('create_chat')
def create_chat(data):
    sp.create_chat(data)

@sio.on('get_chat')
def get_chat(data):
    sp.get_chat(data)

@sio.on('send_message')
def send_message(data):
    sp.send_message(data)

@sio.on('read_message')
def read_message(data):
    sp.read_message(data)

@sio.on('delete_chat')
def delete_chat(data):
    sp.delete_chat(data)

if __name__ == "__main__":
    rp.reload_cities()
    app.run()