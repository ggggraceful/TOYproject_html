from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.gfgawqe.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/write')
def write():
   return render_template('write.html')

@app.route("/write", methods=["POST"])
def write_post():
    title_receive = request.form['title_give']
    image_receive = request.form['image_give']
    heart_receive = request.form['heart_give']
    heart_result_receive = request.form['heart_result_give']
    id_receive = request.form['id_give']
    text_receive = request.form["text_give"]

    doc = {
        'title': title_receive,
        'image': image_receive,
        'heart': heart_receive,
        'heart_result': heart_result_receive,
        'id': id_receive,
        'text': text_receive
    }

    db.writes.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

@app.route("/write", methods=["GET"])
def write_get():
    write_list = list(db.writes.find({}, {'_id': False}))
    return jsonify({'writes': write_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
