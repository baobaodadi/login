
from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response, jsonify
from flask_cors import *

app = Flask(__name__)


CORS(app, supports_credentials=True)

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    if username == 'admin' and password == 'new123':
 # return resp
            return jsonify({"code":0,"message":"OK","data":{"msg":1}})
    else:
            # return redirect(url_for('error'))
            return jsonify({"code":1, "message": "error", "data": {"msg": 0}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
