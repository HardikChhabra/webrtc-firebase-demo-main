from flask import Flask, render_template, redirect, request, session
from sqlalchemy import create_engine, text
import os

engine = create_engine("mysql+pymysql://SPARTAN_suddenlyas:8eeacd533d88e5312f8cf57eec79f173bddf8e01@j5l.h.filess.io:3307/SPARTAN_suddenlyas?charset=utf8mb4")

app = Flask(__name__)
app.secret_key = "best_team"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


def load_users_from_db():
      with engine.connect() as conn:
        result = conn.execute(text('select * from users'))
        USERS = []
        for row in result.all():
          USERS.append(row._mapping)
        return USERS


def User(username, password):
    users = load_users_from_db()
    for i in users:
        if i['name'] == username and i['password'] == password:
            return True      
    return False


@app.route('/dashboard')
def dashboard(username = "Developer"):
    if 'user_id' in session:
        return render_template('dashboard.html', name = username)
    return redirect('/')
        

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/createroom')
def createroom():
    if 'user_id' in session:
        os.system("npm run dev")
        return redirect(':3000')
    return redirect('/')


@app.route('/joinroom')
def joinroom():
    if 'user_id' in session:
        return render_template('joinRoom.html')
    return redirect('/')


@app.route('/forgot_pwd')
def forgot_pwd():
    return render_template('forgot_pwd.html')


@app.route('/signIn', methods=['POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('user_id')
        password = request.form.get('password')
        user = User(username, password)
        if user:
            session['user_id'] = 0
            return dashboard(username)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/joinroomwithid', methods=['POST'])
def joinroomwithid():
    if 'user_id' in session:
        if request.method == 'POST':
            room_id = request.form.get('room_id')
            return redirect(f'/createroom?roomID={room_id}')


if __name__ == '__main__':
    print("I am inside if")
    app.run()