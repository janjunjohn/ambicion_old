import datetime
from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

app = Flask(__name__)
year = datetime.datetime.now().year

EMAIL = os.environ['PYTHON_EMAIL']
EMAIL_PASS = os.environ['EMAIL_PASS']
AMBICION_EMAIL = os.environ['AMBICION_EMAIL']


@app.route('/')
def home():
    return render_template('index.html', year=year)


@app.route('/ai-data-samples')
def sample():
    return render_template('samples.html', year=year)


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

        charset = 'iso-2022-jp'
        msg = MIMEText(f'お名前: {username} \n'
                       f'Email: {user_email} \n'
                       f'ユニフォーム: {uniform} {socks} \n'
                       f'枚数: {number} \n'
                       f'生地: {fabric} \n'
                       f'襟: {neck} \n'
                       f'袖: {sleeve} \n'
                       f'備考: {message} \n',
                       'plain',
                       charset
                       )
        msg['Subject'] = Header(f'{username} 様', charset)

        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:  # choose particular mail sever and port num

            connection.starttls()  # start Transport Layer Security
            connection.login(user=EMAIL, password=EMAIL_PASS)  # login to your email account
            connection.sendmail(from_addr=EMAIL,  # send an email
                                to_addrs=AMBICION_EMAIL,
                                msg=msg.as_string()
                                )
        return render_template('order_page.html', submitted=True, username=username)

    return render_template('order_page.html', year=year)


@app.route('/about')
def about():
    return render_template('about.html', year=year)





if __name__ == '__main__':
    app.run(debug=True)