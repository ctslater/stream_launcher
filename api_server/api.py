
from flask import Flask
app = Flask(__name__)

import os
from flask import json
import kubernetes

DEBUG = os.getenv("DEBUG") is not None

# For use in a running pod
if not DEBUG:
    kubernetes.config.incluster_config.load_incluster_config()
    v1 = kubernetes.client.CoreV1Api()
else:
    print("----------")
    print("DEBUG mode")
    print("----------")
    from api_server.mock import MockKubernetesAPI
    v1 = MockKubernetesAPI()

# For testing with token in ~/.kube/config
# kubernetes.config.load_kube_config()

status = {"kafka": ("Running", "green"),
          "dome": ("Opening", "yellow"),
          "alerts": ("Stopped", "red")}

@app.route("/")
def api():
    return "This is the API server."

@app.route("/system_status")
def system_status():
    return json.dumps(status)

@app.route("/pods")
def pods():

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

