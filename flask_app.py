from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "IR Bank API is up and running!"

