

Front end for launching filter instances via Kubernetes.

Beware, I have no idea how to use React.

Development environment
-----------------------

I use `npm start` in the root directory to start the front end server on
localhost:3000, then `FLASK_APP=api_server/api.py flask run` to start the API
server. The node server proxies the requests it doesn't have routes for to the
API server at localhost:5000.

With uwsgi: `PYTHONHOME=/Users/ctslater/miniconda/envs/py36 uwsgi uwsgi.ini`

Setting the environment variable `DEBUG` when calling uwsgi will cause flask to
use internal mocks for the Kubernetes APIs, to enable stand-alone testing.

Python tests can be run with `DEBUG=1 pytest tests`, which will likely require setting
up the `api_server` package directory with `pip install -e .`.

