from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import jwt
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename
app = Flask(__name__)

from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
client = MongoClient('15.164.230.150', 27017, username="test", password="sparta")
# client = MongoClient('mongodb+srv://test:sparta@cluster0.zp3grhz.mongodb.net/cluster0?retryWrites=true&w=majority')
# 은 DB
# client = MongoClient('mongodb+srv://test:sparta@cluster0.gfgawqe.mongodb.net/?retryWrites=true&w=majority', 27017, username="test", password="sparta")
db = client.GooddaytoWalk
# SECRET_KEY = 'SPARTA'
# db = client.login
# 맥북사용자 필요
# import certifi
# ca = certifi.where()
#
# 잘모르는거
# app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['UPLOAD_FOLDER'] = "./static/profile_pics"


# http://localhost:5000/  index.html

# @app.route('/')
# def home():
#     return render_template('login.html')



#################################
##  HTML을 주는 부분             ##
#################################

# @app.route('/')
# def home():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"username": payload["id"]})
#         # user_info = db.user.find_one({"id": payload['id']})
#         return render_template('login.html', user_info=user_info)
#         # return render_template('index.html', nickname=user_info["nick"])
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

# @app.route('/login')
# def login():
#     msg = request.args.get("msg")
#     return render_template('login.html', msg=msg)


@app.route('/walk', methods=['POST'])
def test_post():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    address_receive = request.form['address_give']
    city_receive = request.form['city_give']
    runtime_receive = request.form['runtime_give']
    difficulty_receive = request.form['difficulty_give']
    print(title_receive)
    print(comment_receive)
    print(address_receive)
    print(city_receive)
    print(runtime_receive)
    print(difficulty_receive)

    # 파일업로드 서버쪽 받기 코드
    file = request.files["file_give"]

    # 확장자명 취하기
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}'
    save_to = f'static/{filename}.{extension}'

    file.save(save_to)

    doc={
        'title':title_receive,
        'comment':comment_receive,
        'address':address_receive,
        'city': city_receive,
        'runtime': runtime_receive,
        'difficulty':difficulty_receive,
        'file': f"{filename}.{extension}"
    }
    db.GooddaytoWalk.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '저장완료!'})



@app.route("/walk_get", methods=["GET"])
def walk_get():
    walk_list = list(db.GooddaytoWalk.find({},{'_id': False}))
    return jsonify({'walk':walk_list})

#################################
##  로그인을 위한 API            ##
#################################
# prac 버전
# def api_login():
#     id_receive = request.form['id_give']
#     pw_receive = request.form['pw_give']
#
#     # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
#     pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
#
#     # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
#     result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
#
#     # 찾으면 JWT 토큰을 만들어 발급합니다.
#     if result is not None:
#         # JWT 토큰에는, payload와 시크릿키가 필요합니다.
#         # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
#         # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
#         # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
#         payload = {
#             'id': id_receive,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
#         }
#         token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
#
#         # token을 줍니다.
#         return jsonify({'result': 'success', 'token': token})
#     # 찾지 못하면
#     else:
#         return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
# @app.route('/sign_in', methods=['POST'])
# def sign_in():
#     # 로그인
#     username_receive = request.form['username_give']
#     password_receive = request.form['password_give']
#
#     pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
#     result = db.users.find_one({'username': username_receive, 'password': pw_hash})
#
#     if result is not None:
#         payload = {
#          'id': username_receive,
#          'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
#         }
#         token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
#
#         return jsonify({'result': 'success', 'token': token})
#     # 찾지 못하면
#     else:
#         return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.

# prac버전
# @app.route('/api/register', methods=['POST'])
# def api_register():
#     id_receive = request.form['id_give']
#     pw_receive = request.form['pw_give']
#     nickname_receive = request.form['nickname_give']
#
#     pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
#
#     db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})
#
#     return jsonify({'result': 'success'})

# @app.route('/sign_up/save', methods=['POST'])
# def sign_up():
#     username_receive = request.form['username_give']
#     password_receive = request.form['password_give']
#
#     password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
#     doc = {
#         "username": username_receive,
#         "password": password_hash,
#     }
#     db.login.insert_one(doc)
#     # db.GooddaytoWalk.insert_one(doc)
#     return jsonify({'result': 'success'})


# @app.route('/sign_up/check_dup', methods=['POST'])
# def check_dup():
#     username_receive = request.form['username_give']
#     exists = bool(db.users.find_one({"username": username_receive}))
#     return jsonify({'result': 'success', 'exists': exists})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)



