import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient

# 플라스크 웹 서버 생성하기
app = Flask(__name__)

# mongodb 추가
client = MongoClient('localhost', 27017)
db = client.get_database('sparta')


# API 추가
@app.route('/', methods=['GET'])  # 데코레이터 문법
def index():  # 함수 이름은 고유해야 한다
    memos = list(db.articles.find({}, {'_id': False}))
    return render_template('index.html', test='테스트', memos=memos)


# 아티클 추가 API
@app.route('/memo', methods=['POST'])
def save_memo():
    form = request.form
    url_receive = form['url_give']
    comment_receive = form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    response = requests.get(
        url_receive,
        headers=headers
    )
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')
    url = soup.select_one('meta[property="og:url"]')
    image = soup.select_one('meta[property="og:image"]')
    description = soup.select_one('meta[property="og:description"]')
    print(title['content'])
    print(url['content'])
    print(image['content'])
    print(description['content'])
    document = {
        'title': title['content'],
        'image': image['content'],
        'description': description['content'],
        'url': url['content'],
        'comment': comment_receive,
    }
    db.articles.insert_one(document)
    return jsonify(
        {'result': 'success', 'msg': '저장했습니다.'}
    )

@app.route('/memo', methods=['GET'])
def list_memo():
    memos = list(db.articles.find({}, {'_id': False}))
    result = {
        'result': 'success',
        'articles': memos,
    }

    return jsonify(result)


# app.py 파일을 직접 실행시킬 때 동작시킴
# 이 코드가 가장 아랫부분
if __name__ == '__main__':
    app.run(
        '0.0.0.0',  # 모든 IP에서 오는 요청을 허용
        7000,  # 플라스크 웹 서버는 7000번 포트 사용
        debug=True,  # 에러 발생 시 에러 로그 보여줌
    )