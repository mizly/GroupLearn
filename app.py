from flask import Flask, render_template, request
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

auth = pyrebase.initialize_app(config).auth()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        pwd_confirm = request.form['pwd_confirm']

        if pwd != pwd_confirm:
            return render_template('signup.html', confirmFail=True)
        
        user = auth.create_user_with_email_and_password(email, pwd)

        

    return render_template('signup.html', confirmFail=False)


if __name__ == '__main__':
    app.run(debug=True)