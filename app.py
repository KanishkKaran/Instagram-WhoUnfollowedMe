from flask import Flask, render_template, request
import json
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

@app.route("/", methods=["GET", "POST"])
def index():
    result_file = None
    if request.method == "POST":
        followers_file = request.files["followers"]
        following_file = request.files["following"]

        followers_data = json.load(followers_file)
        following_data = json.load(following_file)

        followers_usernames = {
            item["string_list_data"][0]["value"]
            for item in followers_data
            if item.get("string_list_data")
        }
        following_usernames = {
            item["string_list_data"][0]["value"]
            for item in following_data.get("relationships_following", [])
            if item.get("string_list_data")
        }

        not_following_back = sorted(following_usernames - followers_usernames)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # ✅ Ensure the 'static' folder exists before writing the file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        result_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"unfollowers_{timestamp}.csv")
        with open(result_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username"])
            for user in not_following_back:
                writer.writerow([user])

        result_file = '/' + result_file_path

    return render_template("index.html", result_file=result_file)

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

