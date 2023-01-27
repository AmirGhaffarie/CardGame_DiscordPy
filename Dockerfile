FROM python:3.10-buster

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/CardGame
COPY requirements.txt start-server.sh /opt/app/
RUN chmod 755 /opt/app/start-server.sh
COPY .pip_cache /opt/app/pip_cache/
COPY CardGame /opt/app/CardGame/
WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache

STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]