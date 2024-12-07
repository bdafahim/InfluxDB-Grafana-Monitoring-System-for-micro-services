from flask import Flask, jsonify, request
import os
import requests
from prometheus_client import Counter, generate_latest
from prometheus_client import start_http_server
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


app = Flask(__name__)

# Environment variables for InfluxDB configuration
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "n8oq7g0atJjfvnGVrFjSIOecH2qq20DyNDtanHpp5JQnChGsLJYpaRvx5nXqCZc3QrntRxePjcy9zMCPzt4_lQ==")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "my-bucket")

# Initialize InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
# Prometheus metrics
#REQUEST_COUNT = Counter("top_universities_requests_total", "Total requests to top-universities", ['endpoint'])

RANKING_UPLOADER_URL = os.getenv("RANKING_UPLOADER_URL", "http://ranking-uploader:4200/rankings")

DEFAULT_TOP_N = int(os.getenv("TOP_N", 5))

@app.route("/top", methods=["GET"])
def get_top_universities():
    """Fetch top N universities from rankings."""
    #REQUEST_COUNT.labels(endpoint="/top").inc()
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


'''@app.route("/metrics", methods=["GET"])
def metrics():
    """Expose Prometheus metrics."""
    return generate_latest(), 200'''

if __name__ == "__main__":
    # Start Prometheus metrics server on 8001
    #start_http_server(8001)
    app.run(host="0.0.0.0", port=4201)
