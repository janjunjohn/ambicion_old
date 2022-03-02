import datetime
from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

PYTHON_EMAIL = os.environ['PYTHON_EMAIL']
AMBICION_EMAIL = os.environ['AMBICION_EMAIL']
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = SENDGRID_API_KEY
app.config['MAIL_DEFAULT_SENDER'] = PYTHON_EMAIL

mail = Mail(app)  # Flask-Mail

year = datetime.datetime.now().year


@app.route('/')
def home():
    return render_template('index.html', year=year)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        username = request.form['username']
        user_email = request.form['email']
        uniform = request.form['form-uniform']
        socks = request.form['form-socks']
        number = request.form['form-number']
        fabric = request.form['form-fabric']
        neck = request.form['form-neck']
        sleeve = request.form['form-sleeve']
        message = request.form['free-text']

        msg = Message(f'{username} 様',
                      recipients=[AMBICION_EMAIL])
        msg.body = f'お名前: {username} \n' \
                   f'Email: {user_email} \n' \
                   f'ユニフォーム: {uniform} {socks} \n' \
                   f'枚数: {number} \n' \
                   f'生地: {fabric} \n' \
                   f'襟: {neck} \n' \
                   f'袖: {sleeve} \n' \
                   f'備考: {message} \n'
        mail.send(msg)
        return render_template('order_page.html', submitted=True, username=username)

    return render_template('order_page.html', year=year)


@app.route('/about')
def about():
    return render_template('about.html', year=year)





if __name__ == '__main__':
    app.run(debug=True)