from flask import Flask, render_template, url_for

app = Flask(__name__)

menu = ['Установка', 'Первое приложение', 'Обратная связь']


@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)

@app.route('/about',)
def about():
    print(url_for('about'))
    return render_template('about.html', title='О сайте', menu=menu)

# @app.route('/profile/<username>')
# @app.route('/profile/<int:username>')
# @app.route('/profile/<int:username>/<path>')
# @app.route('/profile/<float:username>')
@app.route('/profile/<path:username>') #/profile/OverLord</1234/23423>
def profile(username):
    return f'Пользователь: {username}'

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))


if __name__ == '__main__':
    app.run(debug=True)
