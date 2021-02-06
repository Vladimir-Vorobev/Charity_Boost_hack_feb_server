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

@app.route('/get_projects/', methods = ['GET'])
def get_projects():
    return rp.get_projects()

@app.route('/get_my_now_projects/', methods = ['POST'])
def get_my_now_projects():
    return rp.get_my_now_projects(request.data)

# @app.route('/user/<id>/')
# def user_profile(id):
#     return rp.user_profile(id)

# @sio.on('smth')
# def create_room(data):
#     sp.do_smth(data)

if __name__ == "__main__":
    app.run()