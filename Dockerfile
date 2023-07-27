ARG ALPINE_VERSION=3.18
FROM alpine:${ALPINE_VERSION} as prod

ARG VIRTUAL_PIP_INSTALL_DEPS=pip-install-deps
RUN apk update && \
    apk add --no-cache \
        curl \
        gcompat \
        curl \
        python3 \
        libaio \
        wget \
        unzip \
        py3-pip \
        tzdata

WORKDIR /opt/oracle

RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \ 
    unzip instantclient-basiclite-linuxx64.zip && \
    rm instantclient-basiclite-linuxx64.zip && \
    mv /opt/oracle/instantclient* /opt/oracle/instantclient && \
    cd /opt/oracle/instantclient && \
    rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
    mkdir /etc/ld.so.conf.d && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ln -s /opt/oracle/instantclient /opt/oracle/instantclient/lib

ENV LD_LIBRARY_PATH /opt/oracle/instantclient
ENV ORACLE_HOME /opt/oracle/instantclient
ENV PATH $PATH:/opt/oracle/instantclient

RUN mkdir -p /app
WORKDIR /app
COPY . ${WORKDIR}

RUN apk add --no-cache --virtual "${VIRTUAL_PIP_INSTALL_DEPS}" \
        gcc \
        build-base \
        musl-dev \
        python3-dev && \
    pip install --upgrade pip && \
    pip install poetry && \
    python3 -m poetry config virtualenvs.in-project true && \
    python3 -m poetry install && \
    apk --purge del "${VIRTUAL_PIP_INSTALL_DEPS}"

RUN addgroup -S dam -g 1000 && \
    adduser -H -S dam -G dam -h /app -s /bin/sh -u 1000 && \
    chown dam:dam /app -R

USER dam

ENV SERVER_PORT 3000
ENV ADDRESS_PREFIX /api
EXPOSE $SERVER_PORT

CMD python3 -m poetry run uvicorn main:app --host=0.0.0.0 --reload --port ${SERVER_PORT}
