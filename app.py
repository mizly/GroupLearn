from flask import Flask, make_response, render_template, request, redirect, url_for
import pyrebase

app = Flask(__name__)

config = {
    'apiKey': "AIzaSyDpMNHBRMH-4Rszj1GhDFU8tjCjfu7fvNQ",
    'authDomain': "lyonhacks.firebaseapp.com",
    'projectId': "lyonhacks",
    'storageBucket': "lyonhacks.appspot.com",
    'messagingSenderId': "852893010100",
    'appId': "1:852893010100:web:0b18139976c45d6ae52fe1",
    'databaseURL': 'lyonhacks-default-rtdb.firebaseio.com'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/verify')
def verify():
    token = request.cookies.get('token')
    user = auth.get_account_info(token)
    print(user)

@app.route('/matches')
def matches():
    pass

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        pwd_confirm = request.form['pwd_confirm']

        if pwd != pwd_confirm:
            return render_template('signup.html', confirmFail=True, weakPwd=False)
        
        try:
            user = auth.create_user_with_email_and_password(email, pwd)
            auth.send_email_verification(user['userToken'])

            data = {'grade': 0, 'subjects': [], 'day_available':[]}
            db.child('users').child(user['userToken']).set(data)
            
            resp = make_response(redirect(url_for('verify')))
            resp.set_cookie('token', user['token'])
            return resp
        except Exception as err:
            print(err)
            if 'WEAK_PASSWORD' in str(err):
                return render_template('signup.html', confirmFail=False, weakPwd=True)

    return render_template('signup.html', confirmFail=False, weakPwd=False)

if __name__ == '__main__':
    app.run(debug=True)