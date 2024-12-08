from flask import Flask, jsonify, request
import os
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


app = Flask(__name__)

# Environment variables for InfluxDB configuration
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://http://influxdb-service-sdx-assignment-ahmedbad.2.rahtiapp.fi:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "n8oq7g0atJjfvnGVrFjSIOecH2qq20DyNDtanHpp5JQnChGsLJYpaRvx5nXqCZc3QrntRxePjcy9zMCPzt4_lQ==")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "my-bucket")

# Initialize InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)


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

    try:
        health = client.health()
        print(f"InfluxDB health: {health}")
    except Exception as e:
        print(f"Failed to connect to InfluxDB: {e}")

    # Send metrics to InfluxDB
    try:
        point = Point("request_count") \
            .tag("endpoint", "/top") \
            .field("university_count", n)
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"Request send to InfluxDB:")
    except Exception as e:
        print(f"Failed to write to InfluxDB: {e}")

    return jsonify(top_universities)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4201)
