from flask import Flask, render_template, request

app = Flask(__name__)

#main page
@app.route("/")
def testing():
    return(render_template("index.html"))

@app.route('/', methods=["POST"])
def my_form_post():
    username = request.form["text"]
    message = request.form["message"]

    with(open("static/messages.txt", "a") as messages):
        if(username != "" and message != ""):
            messages.write("%s: %s" % (username, message))
            messages.write("\n")

    return(render_template("index.html"))
