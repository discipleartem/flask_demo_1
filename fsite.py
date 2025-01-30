from flask import Flask, render_template, request, flash

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

# @app.route('/profile/<username>')
# @app.route('/profile/<int:username>')
# @app.route('/profile/<int:username>/<path>')
# @app.route('/profile/<float:username>')
@app.route('/profile/<path:username>') #/profile/OverLord</1234/23423>
def profile(username):
    return f'Пользователь: {username}'

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')

    return render_template('contact.html', title='Обратная связь', menu=menu)

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))


if __name__ == '__main__':
    app.run(debug=True)
