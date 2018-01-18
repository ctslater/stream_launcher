
from flask import Flask
app = Flask(__name__)

import os
from flask import request, json, Response
import kubernetes
import datetime
import dateutil
import yaml

DEBUG = os.getenv("DEBUG") is not None

if not DEBUG:
    # For use in a running pod
    kubernetes.config.incluster_config.load_incluster_config()
    v1 = kubernetes.client.CoreV1Api()
    # Need this for deployments, maybe?
    v1beta2 = kubernetes.client.AppsV1beta2Api()
else:
    print("----------")
    print("DEBUG mode")
    print("----------")
    from api_server.mock import MockKubernetesAPIv1, MockKubernetesAPIv1beta2
    v1 = MockKubernetesAPIv1()
    v1beta2 = MockKubernetesAPIv1beta2()

# For testing with token in ~/.kube/config
# kubernetes.config.load_kube_config()

# Pull this from some yaml configuration files, eventually
image_data = {}
image_data['alert_stream'] = {"path": "docker.io/ctslater/alert_stream",
                              "name": "alert_stream",
                              "params": ["KAFKA_SERVER", "ALERT_DATA"],
                              "pod_file": "pod_specs/alert_stream.yaml"}
image_data['simple_filter'] = {"path": "docker.io/ctslater/simple_filter",
                               "name": "simple_filter",
                               "pod_file": "pod_specs/simple_filter.yaml",
                               "params": [], }

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

    #ret = v1beta2.list_namespaced_deployment("default", watch=False)
    ret = v1.list_namespaced_pod("default", watch=False)
    #import pdb; pdb.set_trace()
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

@app.route("/images")
def images():
    keys_to_send = ["name", "path", "params"]
    images_out = []
    for image in image_data.values():
        output = {k:v for k,v in image.items() if k in keys_to_send}
        images_out.append(output)

    return json.dumps(images_out)

@app.route("/startPod", methods=['POST'])
def startPod():

    if "image_name" not in request.json:
        return Response(json.dumps({"status": "Error",
                                    "message": "Invalid Request"}),
                        status=400,
                        mimetype='application/json')

    if request.json['image_name'] not in image_data.keys():
        return Response(json.dumps({"status": "Error",
                                    "message": "Image not found"}),
                        status=400,
                        mimetype='application/json')


    requested_image = image_data[request.json['image_name']]
    with open(requested_image['pod_file']) as f:
        pod_spec = yaml.load(f)

    try:
        deployment = v1beta2.create_namespaced_deployment("default", pod_spec)
    except kubernetes.client.rest.ApiException as e:
        error_json = json.dumps({"status": e.status,
                                 "reason": e.reason,
                                 "body": e.body})
        return Response(error_json, status=e.status,
                        mimetype='application/json')

    return Response(json.dumps({"status": 200}),
                    status=200,
                    mimetype='application/json')

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



