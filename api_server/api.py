
from flask import Flask
app = Flask(__name__)

from flask import json
import kubernetes

# For use in a running pod
kubernetes.config.incluster_config.load_incluster_config()

# For testing with token in ~/.kube/config
# kubernetes.config.load_kube_config()

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

@app.route("/")
def api():
    return "This is the API server."

@app.route("/system_status")
def system_status():
    return json.dumps(status)

@app.route("/pods")
def pods():

    v1 = kubernetes.client.CoreV1Api()
    ret = v1.list_namespaced_pod("default", watch=False)
    pods = []
    for item in ret.items:
        pods.append({"name": item.metadata.name,
                     "status": item.status.phase,
                     #"image": item.spec.image,
                     "created": item.metadata.creation_timestamp,
                     "node": item.spec.node_name,
                     #"conditions": item.status.conditions
                    })

    return json.dumps(pods)

