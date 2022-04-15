from flask import Flask, render_template, request
import requests
from requests.structures import CaseInsensitiveDict

CLIENT_ID = "964586066252300308"
CLIENT_SECRET = "XPHuUMzJBHx5jVw8BFMaFsZ_613NymYe"

app = Flask(__name__)

def exchange_code(CLIENT_ID,CLIENT_SECRET,API_ENDPOINT,code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": 'authorization_code',
        "redirect_uri": "http://127.0.0.1:5000/auth?type=discord"
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

    r = requests.post(API_ENDPOINT + '/oauth2/token', data=data, headers = headers)
    r.raise_for_status()
    return r.json()

@app.route("/")
def homepage():
    return(render_template("auth.html"))

@app.route("/auth")
def authpage():
    type = request.args.get('type')
    if type == "discord":
        code = request.args.get('code')
        response = (exchange_code("964586066252300308","XPHuUMzJBHx5jVw8BFMaFsZ_613NymYe","https://discord.com/api/v8",code))

        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Bearer " + response["access_token"]
        resp = requests.get("https://discord.com/api/users/@me", headers=headers)
        bruh = (resp.json())
        return("You have been verified as %s#%s" % (bruh["username"],bruh["discriminator"]))
