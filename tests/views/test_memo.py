import datetime

import jwt

from tests.conftest import db


def test_메모장_저장(client):
    # 테스트용 메모
    # 실제 네이버 서버를 호출하지 않는 mocking 기법 공부해보기
    url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=056&aid=0011048593'
    comment = 'test comment'

    data = {
        'url_give': url,
        'comment_give': comment,
    }

    # 임의의 사용자 JWT 만들기
    expiration_time = datetime.timedelta(hours=1)
    payload = {
        'id': 'tester',
        'exp': datetime.datetime.utcnow() + expiration_time
    }
    # .env 설정과 맞게 jwt 시크릿 설정
    token = jwt.encode(payload, 'secret')
    headers = {
        'authorization': f'Bearer {token}'
    }

    response = client.post(
        '/memo',
        data=data,
        headers=headers
    )

    assert response.status_code == 200

    # mongodb 저장되었는지 확인
    memo = db.articles.find_one(
        {'id': 'tester'}, {'_id': False}
    )
    assert memo['comment'] == comment
