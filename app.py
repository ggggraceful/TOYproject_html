from flask import Flask, render_template, jsonify, request, redirect, url_for
import jwt, hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import certifi

app = Flask(__name__)
ca = certifi.where()

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

from pymongo import MongoClient

SECRET_KEY = 'SPARTA'
client = MongoClient('mongodb+srv://test:sparta@cluster0.gfgawqe.mongodb.net/?retryWrites=true&w=majority', 27017, username="test", password="sparta", tlsCaFile=ca)
db = client.dbsparta


# client = MongoClient('localhost', 27017)
# db = client.GooddaytoWalk

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('login.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
        return render_template('index.html')


@app.route('/index')
def main():
    return render_template('index.html')

# @app.route('/)
# def home():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"username": payload["id"]})
#         return render_template('login.html', user_info=user_info)
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/walk', methods=['POST'])
def test_post():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    address_receive = request.form['address_give']
    city_receive = request.form['city_give']
    runtime_receive = request.form['runtime_give']
    print(title_receive)
    print(comment_receive)
    print(address_receive)
    print(city_receive)
    print(runtime_receive)

    doc={
        'title':title_receive,
        'comment':comment_receive,
        'address':address_receive,
        'city': city_receive,
        'runtime': runtime_receive
    }
    db.GooddaytoWalk.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '저장완료!'})

@app.route("/walk_get", methods=["GET"])
def walk_get():
    walk_list = list(db.GooddaytoWalk.find({},{'_id': False}))
    return jsonify({'walk':walk_list})

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)



@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)

