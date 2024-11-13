from flask import Flask, render_template, url_for, request, redirect, abort, flash, session
import hashlib
import databaser as db

def hash_password(text):
    return hashlib.sha256(text.encode()).hexdigest()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RLGtqsJ8uyil1cllbbR1zXiwZClSbFvr'


@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
    main_menu = [
        {'url': 'login', 'text': 'Войти'},
        {'url': 'index', 'text': 'Выйти'}
    ]
    return render_template('index.html', title='Главная страница', menu=main_menu)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        if session['status'] == 'teacher':
            return redirect(url_for('teacher'))
        elif session['status'] == 'student':
            return redirect(url_for('student'))

    if request.method == 'POST':
        user = db.user_entry(request.form['login_username'], hash_password(request.form['login_password']))
        if user == False:
            return redirect(url_for('login'))
        else:
            session['username'] = user[0]
            session['status'] = user[1]

        return redirect(url_for('student'))

    return render_template('login.html', title='Авторизация')


@app.route('/exit')
def exit():
    session.clear()
    return redirect(url_for('index'))


@app.route('/student')
def student():
    if 'status' not in session:
        return redirect('index')

    if (session['status'] != 'admin') and ('username' not in session or session['status'] != 'student'):
        abort(401)

    username = session['username']
    return render_template('student.html', title=username, username=username)


@app.route('/teacher')
def teacher():
    if 'status' not in session:
        return redirect('index')
    
    if (session['status'] != 'admin') and ('username' not in session or session['status'] != 'teacher'):
        abort(401)

    # students = db.SELECT_USERS()
    # disciplines = db.SELECT_DISCIPLINES()
    # evaluations = db.SELECT_EVALUATIONS()
    # , students=students, disciplines=disciplines, evaluations=evaluations

    username = session['username']
    return render_template('teacher.html', title=username, username=username)


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title='Страница не найдена'), 404


if __name__ == '__main__':
    app.run(debug=True)