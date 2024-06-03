import datetime
import jwt
from flask import request, jsonify
from config import Config
from models import employees

def authenticate(username, password):
    employee = employees.get(username)
    # if employee == None:
    #     return "erorr"
    if employee and employee["password"] == password:
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_EXPIRATION_DELTA)
        }
        print("payload", payload["exp"])
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        return token
    return None

def verify_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    token = authenticate(username, password)
    if token:
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401
