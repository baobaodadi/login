
from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response, jsonify
from flask_cors import *
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
import json

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

class Article(db.Model):
    title = db.Column(db.String(80),primary_key=True)
    content = db.Column(db.Text)

    def __init__(self, title,content):
        self.title = title
        self.content = content


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


@app.route('/user/content', methods=['GET', 'POST'])
def article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title and content:
            inset = Article(title=title, content=content)
            db.session.add(inset)
            db.session.commit()
            return jsonify({"code": 0, "message": "OK", "data": {"msg": 1}})
        else:
            return jsonify({"code": 1, "message": "error", "data": {"msg": 0}})
    # select_ = User.query.filter_by(name=name).first()
    elif request.method == 'GET':
         title = request.args.get('title')
         content = Article.query.filter_by(title=title).first()

         if content:
             return jsonify({"code": 0, "message": "OK", "data": {"title":title,"content": content.content}})
         else:
             return jsonify({"code": 1, "message": "error", "data": {"msg": 0}})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
