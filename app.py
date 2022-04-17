from flask import Flask, make_response, render_template, request, redirect, url_for, jsonify
from requests import HTTPError
import pyrebase

app = Flask(__name__)

config = {
    'apiKey': "AIzaSyDpMNHBRMH-4Rszj1GhDFU8tjCjfu7fvNQ",
    'authDomain': "lyonhacks.firebaseapp.com",
    'projectId': "lyonhacks",
    'storageBucket': "lyonhacks.appspot.com",
    'messagingSenderId': "852893010100",
    'appId': "1:852893010100:web:0b18139976c45d6ae52fe1",
    'databaseURL': 'https://lyonhacks-default-rtdb.firebaseio.com'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/verify')
def verify():
    # if user hasn't logged in yet, it redirects to login page
    try:
        session_id = request.cookies.get('ssid')

        user = auth.sign_in_with_custom_token(session_id)
        accountInfo = auth.get_account_info(user['idToken'])
    except:
        return redirect(url_for('login'))
    
    email = accountInfo['users'][0]['email']
    # checks if the email is not verified
    if not accountInfo['users'][0]['emailVerified']:
        auth.send_email_verification(user['idToken'])
        return render_template('verify.html', email=email)

    return redirect(url_for('notes'))

@app.route('/matches')
def matches():
    return 'cum'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.args)
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        pwd_confirm = request.form['pwd_confirm']

        if pwd != pwd_confirm:
            return render_template('signup.html', confirmFail=True, weakPwd=False)

        try:
            user = auth.create_user_with_email_and_password(email, pwd)
            auth.send_email_verification(user['idToken'])

            data = {'name': name, 'grade': 0, 'subjects': [], 'day_available':[]}
            
            accountInfo = auth.get_account_info(user['idToken'])
            db.child('/users/' + accountInfo['users'][0]['localId'] + '/').push(data, user['idToken'])

            session_id = auth.create_custom_token(accountInfo['users'][0]['localId'])

            resp = make_response(redirect(url_for('verify')))
            resp.set_cookie('ssid', session_id)
            return resp
        except Exception as err:
            print(err)
            if 'WEAK_PASSWORD' in str(err):
                return render_template('signup.html', confirmFail=False, weakPwd=True)

    return render_template('signup.html', confirmFail=False, weakPwd=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        try:
            user = auth.sign_in_with_email_and_password(email, pwd)
            accountInfo = auth.get_account_info(user['idToken'])
            userInfoId = list(db.child('/users/' + accountInfo['users'][0]['localId'] + '/').get(user['idToken']).val())[0]

            session_id = auth.create_custom_token(accountInfo['users'][0]['localId'])

            resp = make_response(redirect(url_for('verify')))
            resp.set_cookie('ssid', session_id)
            return resp
        except HTTPError as e:
            e = str(e)
            if 'EMAIL_NOT_FOUND' in e:
                return render_template('login.html', invalidPwd=True, content='This account doesn\'t exist. Try a different email or create an account.')
            elif 'INVALID_PASSWORD' in e:
                return render_template('login.html', invalidPwd=True, content='Incorrect Password. Double check and try again.')
            elif 'TOO_MANY_ATTEMPTS_TRY_LATER' in e:
                return render_template('login.html', invalidPwd=True, content='Too many unsuccessful login attempts. Please try again later.')
                    
        return redirect(url_for('verify'))
        
    # if user hasn't logged in yet, it redirects to login page
    try:
        session_id = request.cookies.get('ssid')

        user = auth.sign_in_with_custom_token(session_id)
        accountInfo = auth.get_account_info(user['idToken'])
        return redirect(url_for('verify'))
    except Exception as e:
        print(e)
        return render_template('login.html', invalidPwd=False)

if __name__ == '__main__':
    app.run(debug=True)
