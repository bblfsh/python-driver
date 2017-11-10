FROM alpine:3.6

RUN mkdir -p /opt/driver/src && \
    adduser $BUILD_USER -u $BUILD_UID -D -h /opt/driver/src

RUN apk add --no-cache --update python python3 git make

WORKDIR /opt/driver/src
