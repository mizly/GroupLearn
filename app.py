from flask import Flask, render_template
from requests import request
import pyrebase

app = Flask(__name__)

config = {
    'apiKey': "AIzaSyDpMNHBRMH-4Rszj1GhDFU8tjCjfu7fvNQ",
    'authDomain': "lyonhacks.firebaseapp.com",
    'projectId': "lyonhacks",
    'storageBucket': "lyonhacks.appspot.com",
    'messagingSenderId': "852893010100",
    'appId': "1:852893010100:web:0b18139976c45d6ae52fe1"
}

auth = pyrebase.initialize_app(config).auth()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['name']
        pwd = request.form['name']
        pwd_confirm = request.form['name']

        if pwd != pwd_confirm:
            return render_template('signup.html', confirmFail=True)

        

    return 'lyonhacks 2022'


if __name__ == '__main__':
    app.run(debug=True)