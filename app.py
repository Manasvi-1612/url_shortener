from time import time

from flask import Flask, redirect,render_template,request,jsonify

from services import canonicalize, generate_short_code,resolve_collision

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

url_store = {} # In-memory store for URL mappings


@app.route("/api/shorten",methods = ["POST"])
def generate_url():

    data = request.get_json()
    
    long_url = data["long_url"]
    expiry = data["expiry"]
    alias = data["alias"]


    if not long_url:
        return jsonify({"error":"Long URL is required"}),400


    if alias:
        if alias in url_store:
            existing_url = url_store[alias]["long_url"]

            if existing_url != long_url:
                return jsonify({"error":"Alias already in use for a different URL"}),400
            
            url_store[alias]["expiry"] = expiry
            return jsonify({"short_url": alias}), 200

    long_url = canonicalize(long_url)
    short_code = generate_short_code(long_url)  


    if short_code in url_store:
        if url_store[short_code]["long_url"] == long_url:
            url_store[short_code]["expiry"] = expiry
            print("already exists",url_store)
            return jsonify({"short_url": short_code}), 200

        # Collision handling
        attempt = 1
        while short_code in url_store and url_store[short_code]["long_url"] != long_url:
            short_code = resolve_collision(long_url, attempt)
            attempt += 1
    
    url_store[short_code]={
        "long_url": long_url,
        "expiry": expiry
    }

    print(url_store) 

    return jsonify({"short_url": short_code}), 201


@app.route("/<short_code>")
def redirect_to_long_url(short_code):
    if short_code not in url_store:
        return "URL not found", 404

    url_data = url_store[short_code]
    long_url = url_data["long_url"]
    expiry = url_data["expiry"]

    # Check for expiry
    if expiry and expiry < time.time():
        del url_store[short_code]  # Clean up expired entry
        return "URL has expired", 410

    return redirect(long_url)

@app.route("/api/links", methods=["GET"])
def list_links(): 
    return jsonify(url_store), 200

if __name__ == "__main__":
    app.run(debug=True)        