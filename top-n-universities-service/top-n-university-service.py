from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

RANKING_UPLOADER_URL = os.getenv("RANKING_UPLOADER_URL", "http://ranking-uploader:4200/rankings")

DEFAULT_TOP_N = int(os.getenv("TOP_N", 5))

@app.route("/top", methods=["GET"])
def get_top_universities():
    """Fetch top N universities from rankings."""
    response = requests.get(RANKING_UPLOADER_URL)
    rankings = response.json()

    # Get 'n' from query parameter or use the default value
    n = request.args.get("n", DEFAULT_TOP_N, type=int)
    top_universities = rankings[:n]
    return jsonify(top_universities)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4201)
