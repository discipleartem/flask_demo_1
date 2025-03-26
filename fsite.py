import os
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, g
from FDataBase import FDataBase, sqlite3
#run app from terminal:
#flask --app fsite run --debug

#Конфигурация базы данных
DATABASE = '/tmp/fsite.db'
DEBUG = True
SECRET_KEY = 'fb3a2ca34f1d0492ad3395e7951966'

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret_key'
#app.secret_key = 'b85ac7cb2c5719f8fb3a2ca34f1d0492ad3395e795196613336d80ced3cc189a'
app.config.from_object(__name__) # __name__ это ссылка на текущий модуль
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fsite.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
"""
в python консоле:
from fsite import create_db
create_db()
"""


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


@app.route('/')
def index():
    # print(url_for('index'))
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())

@app.teardown_appcontext # декоратор, который вызывается при завершении запроса (уничтожении контекста приложения)
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/about',)
def about():
    # print(url_for('about'))
    return render_template('about.html', title='О сайте', menu=menu)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')

    return render_template('contact.html', title='Обратная связь', menu=menu)

# @app.route('/profile/<int:username>')
# @app.route('/profile/<int:username>/<path>')
# @app.route('/profile/<float:username>')
# @app.route('/profile/<path:username>') #/profile/OverLord</1234/23423>
@app.route('/profile/<username>')
def profile(username):
    if 'user_logged' not in session or session['user_logged'] != username:
        abort(401)

    return f'Профиль пользователя: {username}'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'user_logged' in session:
        return redirect(url_for('profile', username=session['user_logged']))
    elif request.method == 'POST' and request.form['username'] == 'admin' and request.form['password'] == '12345':
        session['user_logged'] = request.form['username']
        return redirect(url_for('profile', username=session['user_logged']))

    return render_template('login.html', title='Авторизация', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu, error=error), 404


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', title='Добавление статьи', menu=dbase.getMenu())


@app.route('/post/<int:id_post>')
def show_post(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))


if __name__ == '__main__':
    app.run(debug=True)
