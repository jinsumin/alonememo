from flask import Flask, render_template

# 플라스크 웹 서버 생성하기
app = Flask(__name__)

# API 추가
@app.route('/', methods=['GET'])  # 데코레이터 문법
def index():  # 함수 이름은 고유해야 한다
    return render_template('index.html', test='테스트')


# app.py 파일을 직접 실행시킬 때 동작시킴
# 이 코드가 가장 아랫부분
if __name__ == '__main__':
    app.run(
        '0.0.0.0',  # 모든 IP에서 오는 요청을 허용
        7000,  # 플라스크 웹 서버는 7000번 포트 사용
        debug=True,  # 에러 발생 시 에러 로그 보여줌
    )
