from flask import Flask, request, jsonify
import json

app = Flask(__name__, static_folder="../FrontEnd", static_url_path="")

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/save", methods=["POST"])
def save():
    return jsonify({"ok":True})

app.run(debug=True)
