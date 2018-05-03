FROM alpine:3.7

RUN mkdir -p /opt/driver/src && \
    adduser $BUILD_USER -u $BUILD_UID -D -h /opt/driver/src

RUN apk add --no-cache --update python python3 py-pip py2-pip git make

WORKDIR /opt/driver/src
