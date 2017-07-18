FROM alpine:3.6

RUN mkdir -p /opt/driver/src && \
    adduser $BUILD_USER -u $BUILD_UID -D -h /opt/driver/src

RUN apk add --no-cache --update python python-dev python3 python3-dev py-pip py2-pip git build-base bash
RUN pip3 install git+https://github.com/python/mypy.git@0bb2d1680e8b9522108b38d203cb73021a617e64#egg=mypy-lang

WORKDIR /opt/driver/src
