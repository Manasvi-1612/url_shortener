from flask import Flask,render_template,request,jsonify

import hashlib
import base62

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/api/shorten",methods = ["POST"])
def generate_url():

    data = request.get_json()
    
    long_url = data["long_url"]
    expiry = data["expiry"]
    alias = data["alias"]

    if alias:
        return {
            "short_url": alias
        }

    res = hashlib.md5(long_url.encode('utf-8')).hexdigest()
    hash_int = int(res, 16)

    short_code = base62.encode(hash_int)

    return {
        "short_url":short_code
    }

if __name__ == "__main__":
    app.run(debug=True)        