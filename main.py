import datetime
from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
import requests

PYTHON_EMAIL = os.environ['PYTHON_EMAIL']
AMBICION_EMAIL = os.environ['AMBICION_EMAIL']
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
RECAPTCHA_SITEKEY = os.environ['RECAPTCHA_SITEKEY']
RECAPTCHA_SECRET_KEY = os.environ['RECAPTCHA_SECRET_KEY']
RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'
BLOCK_USERNAME = ['Eric Jones', 'Mike Taft']

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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        recaptcha_response = request.form['g-recaptcha-response']
        is_success_recaptcha = requests.post(url=RECAPTCHA_URL, params={'secret': RECAPTCHA_SECRET_KEY, 'response': recaptcha_response}).json()['success']
        
        if is_success_recaptcha:
            username = request.form['username']
            user_email = request.form['email']
            message = request.form['free-text']

            msg = Message(f'質問：{username} 様',
                        recipients=[AMBICION_EMAIL])
            msg.body = f'お名前: {username} \n' \
                    f'Email: {user_email} \n' \
                    f'備考: {message} \n'
            if not username in BLOCK_USERNAME:
                mail.send(msg)
            return render_template('index.html', submitted='success', username=username, year=year, sitekey=RECAPTCHA_SITEKEY)
        else:
            return render_template('index.html', submitted='failed', year=year, sitekey=RECAPTCHA_SITEKEY)

    return render_template('index.html', year=year, sitekey=RECAPTCHA_SITEKEY)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        recaptcha_response = request.form['g-recaptcha-response']
        is_success_recaptcha = requests.post(url=RECAPTCHA_URL, params={'secret': RECAPTCHA_SECRET_KEY, 'response': recaptcha_response}).json()['success']
        
        if is_success_recaptcha:
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
            return render_template('order_page.html', submitted='success', username=username, year=year, sitekey=RECAPTCHA_SITEKEY)
        else:
            return render_template('order_page.html', submitted='failed', year=year, sitekey=RECAPTCHA_SITEKEY)

    return render_template('order_page.html', year=year, sitekey=RECAPTCHA_SITEKEY)


@app.route('/about')
def about():
    return render_template('about.html', year=year)





if __name__ == '__main__':
    app.run(debug=True)