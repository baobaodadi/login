
from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response, jsonify
from flask_cors import *
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:new123@localhost/mysite?charset=utf8mb4'
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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)

    def __init__(self, title,content):
        self.title = title
        self.content = content


# CORS(app, supports_credentials=True)

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']



        select_=User.query.filter_by(username=username).first()

        if password == select_.email:
                # session['username'] = username
                response = make_response(jsonify({"code":0,"message":"OK","data":{"msg":1}}))
                expire_date = datetime.datetime.now()
                expire_date = expire_date + datetime.timedelta(days=90)
                response.set_cookie('framework', 'flask',expires=expire_date)
                return response
        else:
                response = make_response(jsonify({"code":1, "message": "error","data": {"msg": 0}}))
                return response
    else:
        cookieName=request.cookies.get('framework')
        print cookieName
        if cookieName:
            return make_response(jsonify({"code": 0, "message": "OK", "data": {"msg": 1}}))
        else:
            return make_response(jsonify({"code": 1, "message": "error", "data": {"msg": 0}}))


@app.route('/user/content', methods=['GET', 'POST'])
def article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title and content:
            inset = Article(title=title, content=content)
            db.session.add(inset)
            db.session.commit()
            response = make_response(jsonify({"code": 0, "message": "OK", "data": {"msg": 1}}))
        else:
            response = make_response(jsonify({"code": 1, "message": "error", "data": {"msg": 0}}))
    # select_ = User.query.filter_by(name=name).first()
    elif request.method == 'GET':
         id = request.args.get('id')
         content = Article.query.filter_by(id=id).first()

         if content:
             response = make_response(jsonify({"code": 0, "message": "OK", "data": {"title":content.title,"content": content.content}}))
         else:
             response = make_response(jsonify({"code": 1, "message": "error", "data": {"msg": 0}}))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/article/list', methods=['GET'])
def list():
    if request.method == 'GET':
         count =  Article.query.all()
         list=[]
         for data in count:
             articleList = dict()
             articleList[data.id]=data.title
             list.append(articleList)

         if count:
             response = make_response(jsonify({"code": 0, "message": "OK", "data": {"list": list}}))
         else:
             response = make_response(jsonify({"code": 1, "message": "error", "data": {"msg": 0}}))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

if __name__ == '__main__':
    app.run(debug=True)

