FROM alpine:3.6
MAINTAINER source{d}

RUN apk add --no-cache --update python python3 py-pip py2-pip git


ADD build /opt/driver/bin
ADD native/python_package /tmp/python_driver
RUN pip3 install /tmp/python_driver
RUN yes|rm -rf /tmp/python_driver

ADD native/dev_deps /tmp/dev_deps
RUN pip2 install -U /tmp/dev_deps/python-pydetector || pip2 install pydetector-bblfsh==0.10.3
RUN pip3 install -U /tmp/dev_deps/python-pydetector || pip3 install pydetector-bblfsh==0.10.3
RUN yes|rm -rf /tmp/dev_deps

CMD /opt/driver/bin/driver
