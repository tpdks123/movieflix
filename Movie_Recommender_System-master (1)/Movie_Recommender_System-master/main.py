from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

movies = [
    {
        'id': 1,
        'title': 'Inception',
        'poster': 'https://example.com/poster1.jpg',
        'description': 'A thief enters the dreams of others to steal their secrets.',
        'genre': 'Sci-Fi',
        'release_date': '2010-07-16',
        'rating': 8.8
    },
    {
        'id': 2,
        'title': 'The Dark Knight',
        'poster': 'https://example.com/poster2.jpg',
        'description': 'Batman faces the Joker, a criminal mastermind with a dark sense of humor.',
        'genre': 'Action',
        'release_date': '2008-07-18',
        'rating': 9.0
    },
    # ... (더 많은 영화 추가)
]

users = [
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'},
]

# MySQL 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sean:jj001109@localhost/db_movieflix'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

@app.route('/home')
def home():
    return render_template('main.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # 로그인 성공 시 세션에 사용자 정보 저장
            session['user'] = {'id': user.id, 'username': user.username}
            return render_template('main.html')
        else:
            # 로그인 실패 시 에러 메시지 반환
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    pass

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm_password = request.form['confirm_password']

        # 간단한 유효성 검사
        if not username or not password or not confirm_password:
            return render_template('signup.html', error='모든 필드를 입력해주세요.')

        if password != confirm_password:
            return render_template('signup.html', error='비밀번호가 일치하지 않습니다.')

        # 사용자 데이터베이스에 추가
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # 회원가입 후 로그인 페이지로 리다이렉션
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/movieDetails/<int:data_movie_id>')
def movieDetails(data_movie_id):
    # 해당 ID의 영화를 찾음
    return render_template('movieDetails.html', movie_id=data_movie_id)
    # movie = next((m for m in movies if m['id'] == movie_id), None)

    # if movie:
    #     return render_template('MovieDetails.html', movie=movie)
    # else:
    #     # 찾지 못한 경우 404 에러 페이지로 리다이렉션
    #     return redirect(url_for('not_found'))

if __name__ == '__main__':
    app.run(debug=True)
