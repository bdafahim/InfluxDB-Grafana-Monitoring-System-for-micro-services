# InfluxDB-Grafana Monitoring System for top-universities service

This project demonstrates a monitoring system that collects, stores, and visualizes metrics for a service using InfluxDB and Grafana deployed on an OpenShift (Rahti) cluster. It integrates data collection from a microservice (top-universities) and displays insights through a Grafana dashboard.

## Features
InfluxDB: Stores metrics collected from the top-universities microservice.
Grafana: Provides a dashboard to visualize metrics from InfluxDB.
Kubernetes Deployment: Fully containerized and deployed on Rahti/OpenShift.
Token-Based Authentication: Secures access to InfluxDB data.

## Architecture
top-universities: A microservice that collects university ranking data and tracks API request counts.
InfluxDB: A time-series database used to store request count metrics.
Grafana: A visualization tool used to build real-time dashboards.
Kubernetes: Deploys and manages the services in Rahti/OpenShift.

## Prerequisites
Rahti/OpenShift Cluster.
oc CLI installed and configured.
Docker for local development.

## Setup and Deployment
git clone https://github.com/bdafahim/InfluxDB-Grafana-Monitoring-System-for-micro-services.git

## Build and Push Docker Images

docker build -t <dockerhub-username>/university-list:tag-f Dockerfile .
docker push <dockerhub-username>/university-list: tag

docker build -t <dockerhub-username>/top-universities:tag -f Dockerfile .
docker push <dockerhub-username>/top-universities:tag

## Deploy InfluxDB

1. Apply the InfluxDB deployment configuration:

oc apply -f influxdb.yaml

2. Verify the InfluxDB service:

oc get pods
oc get svc influxdb-service

3. Expose InfluxDB to create a route:
oc expose svc influxdb-service



## Deploy Grafana
1. Apply the Grafana deployment configuration:

oc apply -f grafana.yaml

2. Verify the Grafana service:

oc get pods
oc get svc grafana-service
oc get route grafana-route

## Configure Grafana
Configure Grafana
Access Grafana via the route URL:
http://<grafana-route-hostname>
Log in with default credentials (admin/admin123).
Add InfluxDB as a data source:
Select query language as flux
provide the organization and bucket name
Save and test the data source.

## Trigger the top-universities Service

To send a request to the top-universities service and collect metrics, run the following curl command:


curl "http://localhost:4201/top?n=50"

Here:
n=50: Fetches the top 50 universities from the ranking data.
Metrics for this request will be stored in InfluxDB.

##  Create Dashboards in Grafana
After, Save and test the data source.
Click 'building a dashboard'
Copy the query script from influxdb explore
paste it in the query of the dashboard builde of grafana
Select which range of data you want to see

## Architecture diagram
![Architecture Diagram](https://raw.githubusercontent.com/bdafahim/Final-Project-SDS/main/ARCH.drawio.png)

## InfluxDB dashboard
![InfluxDB Dashboard](https://raw.githubusercontent.com/bdafahim/Final-Project-SDS/main/Influxdb%20dashboard.png)

## Grafana dashboard
![InfluxDB Dashboard](https://raw.githubusercontent.com/bdafahim/Final-Project-SDS/main/Grafana%20Dashboard.png)
