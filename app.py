from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'lyonhacks 2022'


if __name__ == '__main__':
    app.run(debug=True)