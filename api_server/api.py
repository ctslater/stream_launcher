
from flask import Flask
app = Flask(__name__)

from flask import json

status = {"kafka": ("Running", "green"),
          "dome": ("Opening", "yellow"),
          "alerts": ("Stopped", "red")}

pod_data = [
  {"name": "kafka-2",
   "node": "cts-spark",
   "status": "Running",
   "restarts": "0",
   "age": "3 hours"},

  {"name": "kafka-3",
   "node": "cts-spark",
   "status": "Stopped",
   "restarts": "3",
   "age": "1 week"},
]

@app.route("/api")
def api():
    return "This is the API server."

@app.route("/api/system_status")
def system_status():
    return json.dumps(status)

@app.route("/api/pods")
def pods():
    return json.dumps(pod_data)

