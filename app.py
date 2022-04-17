from flask import Flask, make_response, render_template, request, redirect, url_for, jsonify
from sort import sort_compabitility
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
    'databaseURL': 'https://lyonhacks-default-rtdb.firebaseio.com',
    'serviceAccount': 'lyonhacks-firebase-adminsdk-iqha5-753e386ab1.json'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify')
def verify():
    if str(request.cookies.get('email')) == 'None' or str(request.cookies.get('email')) == '':
        return redirect(url_for('login'))

    email = request.cookies.get('email')
    password = request.cookies.get('password')
    user = auth.sign_in_with_email_and_password(email, password)
    if not auth.get_account_info(user['idToken'])['users'][0]['emailVerified']:
        auth.send_email_verification(user['idToken'])
        return '<h1 style="font-family: Source Sans Pro;" align="center">Your account has yet to be verified. Check your email to verify this account.</h1>'
    else:
        return redirect(url_for('matches'))

@app.route('/matches')
def matches():
    # if user hasn't logged in yet, it redirects to login page
    try:
        email = request.cookies.get('email')
        password = request.cookies.get('password')
        user = auth.sign_in_with_email_and_password(email, password)
        accountInfo = auth.get_account_info(user['idToken'])
    except:
        return redirect(url_for('login'))
            
    user_info = list(db.child('/users/' + accountInfo['users'][0]['localId'] + '/').get(user['idToken']).val().values())[0]
    
    scores = sort_compabitility(user_info, **dict(db.child('users').get().val()))
    scores = dict(sorted(scores.items(), key=lambda item: item[1]))

    matches = []
    for key in scores:
        matches.append({ 'info': list(db.child('/users/' + key + '/').get().val().values())[0], 'score': scores[key] })

    return render_template('matches.html', matches=matches)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        email = request.cookies.get('email')
        password = request.cookies.get('password')
        user = auth.sign_in_with_email_and_password(email, password)
        accountInfo = auth.get_account_info(user['idToken'])

        name = request.form['name']
        grade = request.form['grade']
        subjects = request.form['subjects'].split(',')

        day_available = [[False]*24]*7
        for key in dict(request.form):
            if '-' in key:
                print(key)
                pos = key.split('-')
                day_available[int(pos[0])][int(pos[1])] = True

        local = list(db.child('/users/' + accountInfo['users'][0]['localId'] + '/').get(user['idToken']).val().keys())[0]
        print(local)

        data = {local: {'name': name, 'grade': grade, 'subjects': subjects, 'day_available': day_available}}
        db.child('/users/' + accountInfo['users'][0]['localId'] + '/').update(data, user['idToken'])

        user_info = list(db.child('/users/' + accountInfo['users'][0]['localId'] + '/').get(user['idToken']).val().values())[0]

        return render_template('profile.html', user=user_info, profileUpdated=False)

    # if user hasn't logged in yet, it redirects to login page
    try:
        email = request.cookies.get('email')
        password = request.cookies.get('password')
        user = auth.sign_in_with_email_and_password(email, password)
        accountInfo = auth.get_account_info(user['idToken'])
    except:
        return redirect(url_for('login'))
                
    user_info = list(db.child('/users/' + accountInfo['users'][0]['localId'] + '/').get(user['idToken']).val().values())[0]

    user_info['subjects'] = ','.join(user_info['subjects'])
    return render_template('profile.html', user=user_info, profileUpdated=False)

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

            data = {'name': name, 'email': email, 'grade': 0, 'subjects': ['all'], 'day_available':[[True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]]}
            
            accountInfo = auth.get_account_info(user['idToken'])
            db.child('/users/' + accountInfo['users'][0]['localId'] + '/').push(data, user['idToken'])

            resp = make_response(redirect(url_for('verify')))
            resp.set_cookie('email', email)
            resp.set_cookie('password', pwd)
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

            resp = make_response(redirect(url_for('verify')))
            resp.set_cookie('email', email)
            resp.set_cookie('password', password)
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
        
    try:
        email = request.cookies.get('email')
        password = request.cookies.get('password')
        user = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('matches'))
    except:
        return render_template('login.html', invalidPwd=False)

@app.route("/listing")
def listing():
    return(render_template("listing.html"))

if __name__ == '__main__':
    app.run(debug=True)
