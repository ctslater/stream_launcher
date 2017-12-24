

Front end for launching filter instances via Kubernetes.

Beware, I have no idea how to use React.

Development environment
-----------------------

I use `npm start` in the root directory to start the front end server on
localhost:3000, then `FLASK_APP=api_server/api.py flask run` to start the API
server. The node server proxies the requests it doesn't have routes for to the
API server at localhost:5000.

With uwsgi for debugging: `PYTHONHOME=/Users/ctslater/miniconda/envs/py36 uwsgi uwsgi.ini`

