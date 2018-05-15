
from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response, jsonify
from flask_cors import *
import MySQLdb
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:new123@localhost/mysite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    phone = db.Column(db.String(32), nullable=False)

    def __init__(self, username, email, phone):
        self.username = username
        self.email = email
        self.phone = phone


CORS(app, supports_credentials=True)

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    select_=User.query.filter_by(username=username).first()

    if password == select_.email:
            print(password)
            return jsonify({"code":0,"message":"OK","data":{"msg":1}})
    else:
            return jsonify({"code":1, "message": "error", "data": {"msg": 0}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
