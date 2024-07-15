from unittest import result
from auth import app, sqldb
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime


@app.route('/login')
def login():
    auth = request.authorization
    #print(auth)

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    mysql_obj = sqldb.MySQLManager()
    result = mysql_obj.find_one(auth.username, auth.password)

    if result[1] == auth.username:
        user = result
    else:
        user = None

    password = generate_password_hash(user[2], method='sha256')

    if not user:
        print("\nerror at line 201\n")
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(password, auth.password):
        token = jwt.encode({'id': user[1], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])

        print("header = ", request.headers)
        return jsonify({'token': token, 'short_id': user[0]})

    print("\nerror at line 209\n")
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route("/verify_user")
def verify_user():
    user = request.json

    mysql_obj = sqldb.MySQLManager()

    result = mysql_obj.find_user(user["username"])

    if result:
        return jsonify({'result': "Found"})
    else:
        return jsonify({'result': "NotFound"})


@app.route("/register", methods=["POST"])
def register():
    user = request.json

    print(user)

    mysql_obj = sqldb.MySQLManager()

    result = mysql_obj.insert_one(user['user_id'], user['username'], user['password_hash'], datetime.datetime.utcnow(), datetime.datetime.utcnow())

    return str(result)
