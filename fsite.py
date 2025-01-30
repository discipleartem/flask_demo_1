from flask import Flask, render_template, request, flash, session, redirect, url_for, abort

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret_key'
app.secret_key = 'b85ac7cb2c5719f8fb3a2ca34f1d0492ad3395e795196613336d80ced3cc189a'

#run app from terminal:
#flask --app fsite run --debug

menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


@app.route('/')
def index():
    # print(url_for('index'))
    return render_template('index.html', menu=menu)

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


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))


if __name__ == '__main__':
    app.run(debug=True)
