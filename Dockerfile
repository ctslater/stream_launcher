
# Stage 1 - Compile react scripts to static artifacts.
FROM node:8.4.0
WORKDIR /opt
# Copy local files into /opt
COPY . .

RUN npm install
RUN npm run build --production


# Stage 2 - uWSGI server running flask app, with react static files.
FROM python:3.6-slim
LABEL maintainer "ctslater@uw.edu"
WORKDIR /opt
COPY . .

# Copy react products.
COPY --from=0 /opt/build build/

# gcc is required to compile uwsgi
# Need /etc/mime.types for serving static files from uwsgi
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y gcc mime-support

RUN pip install --no-cache-dir -r requirements.txt


# Not sure about this part
RUN groupadd -r uwsgi_grp && useradd -r -g uwsgi_grp uwsgi
#RUN chown -R uwsgi:uwsgi_grp /opt/api_server
USER uwsgi

EXPOSE 8000
CMD uwsgi uwsgi.ini

