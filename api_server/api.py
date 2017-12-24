
from flask import Flask
app = Flask(__name__)

import os
from flask import json
import kubernetes
import datetime
import dateutil

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
    # import pdb; pdb.set_trace()
    pods = []
    for item in ret.items:
        pods.append({"name": item.metadata.name,
                     "status": item.status.phase,
                     "image": item.spec.containers[0].image,
                     "created": item.metadata.creation_timestamp,
                     "node": item.spec.node_name,
                     #"conditions": item.status.conditions,
                     "restarts": item.status.container_statuses[0].restart_count,
                     "running_time": format_duration(item.status.start_time)
                    })

    return json.dumps(pods)

# This should get moved to a different file
def format_duration(start_time, now=None):
    if now is None:
        now = datetime.datetime.now(dateutil.tz.tz.tzlocal())

    duration = now - start_time
    if duration.total_seconds()/(24*3600) >= 2.0:
        return "{:.0f} days".format(duration.total_seconds()/3600/24)
    if duration.total_seconds()/(24*3600) >= 1.0:
        return "{:.0f} day".format(duration.total_seconds()/3600/24)
    if duration.total_seconds()/3600 >= 2.0:
        return "{:.0f} hours".format(duration.total_seconds()/3600)
    elif duration.total_seconds()/3600 >= 1.0:
        return "{:.0f} hour".format(duration.total_seconds()/3600)
    elif duration.total_seconds()/60 >= 2.0:
        return "{:.0f} minutes".format(duration.total_seconds()/60)
    elif duration.total_seconds()/60 >= 1.0:
        return "{:.0f} minute".format(duration.total_seconds()/60)
    else:
        return "{:.0f} seconds".format(duration.total_seconds())



