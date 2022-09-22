from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb+srv://test:sparta@cluster0.zp3grhz.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.GooddaytoWalk

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/walk', methods=['POST'])
def test_post():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    address_receive = request.form['address_give']
    city_receive = request.form['city_give']
    runtime_receive = request.form['runtime_give']

    doc={
        'title':title_receive,
        'comment':comment_receive,
        'address':address_receive,
        'city': city_receive,
        'runtime': runtime_receive
    }
    db.GooddaytoWalk.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '저장완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

