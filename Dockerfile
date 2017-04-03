FROM       python:2.7
MAINTAINER Ilya Komarov <mozgitweb@gmail.com>

EXPOSE 5000

ADD . /todo
WORKDIR /todo
RUN pip install flask
RUN pip install -r requirements.txt

#ENTRYPOINT ["/usr/bin/python" , "web/server.py"]
