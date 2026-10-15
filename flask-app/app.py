from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Flask on EC2</h1><p>Served by gunicorn on port 5000</p>"
