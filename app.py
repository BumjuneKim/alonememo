from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['POST'])
def post_article():
    url = request.form['url_give']
    comment = request.form['comment_give']

    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_title = soup.select_one('meta[property="og:title"]')
    og_image = soup.select_one('meta[property="og:image"]')
    og_description = soup.select_one('meta[property="og:description"]')

    new_article = {
        'url': url,
        'title': og_title['content'],
        'image': og_image['content'],
        'description': og_description['content'],
        'comment': comment
    }

    db.articles.insert_one(new_article)
    return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})


@app.route('/memo', methods=['GET'])
def read_articles():
    articles = list(db.articles.find({}, {'_id': 0}))
    return jsonify({
        'result': 'success',
        'articles': articles
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)