FROM quay.io/srcd/basic:latest
MAINTAINER source{d}

RUN apt update
RUN apt install -y python2.7 python2.7-dev python-pip python3 python3-dev \
    python3-six python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install msgpack-python
RUN pip3 install six
RUN pip3 install git+https://github.com/juanjux/python-pydetector.git

RUN pip2 install six
RUN pip2 install git+https://github.com/juanjux/python-pydetector.git

ADD bin /bin

CMD ["python3",  "bin/pyparser.py"]
