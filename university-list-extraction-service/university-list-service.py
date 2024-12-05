from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load the university ranking data
df = pd.read_csv("universities.csv")

@app.route("/rankings", methods=["GET"])
def get_rankings():
    """Return all university rankings as JSON."""
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4200)