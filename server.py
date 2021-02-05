from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from flask_socketio import SocketIO
sio = SocketIO(app, cors_allowed_origins = "*", async_mode='threading')