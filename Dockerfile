# Build vuejs front
FROM node:lts-alpine as node-build
ENV USER=chatsubo
ENV UID=1324
ENV GID=1324

RUN mkdir /build
COPY front /build
WORKDIR /build

RUN npm install && npm run build

# Build python virtualenv
FROM python:3.9.1-alpine3.12 as python-build
RUN apk add --no-cache libffi-dev openssl-dev \
 	mariadb-dev \
 	build-base bash git ca-certificates

RUN pip3 install --upgrade pip setuptools

RUN mkdir /opt/chatsubo
COPY requirements.txt /opt/chatsubo
WORKDIR /opt/chatsubo

RUN pip3 install virtualenv &&\
	 virtualenv venv --python=$(which python3) && \
	./venv/bin/pip install -r ./requirements.txt

# Copy only what's needed
FROM python:3.9.1-alpine3.12
ENV USER=chatsubo
ENV UID=1324
ENV GID=1324
ENV CHATSUBO_PORT=8000

RUN apk add mysql-client \
	mariadb-dev \
	tzdata

RUN addgroup -g "$GID" chatsubo
RUN adduser \
    --disabled-password \
    --gecos "" \
    --ingroup "$USER" \
    --no-create-home \
    --uid "$UID" \
    "$USER"

ADD app /opt/chatsubo/app
COPY docker/entrypoint.sh /opt/chatsubo/docker/entrypoint.sh
COPY --from=node-build /build/dist /opt/chatsubo/front/dist
COPY --from=python-build /opt/chatsubo/venv /opt/chatsubo/venv
WORKDIR /opt/chatsubo

RUN chmod +x /opt/chatsubo/docker/entrypoint.sh
RUN chown -R "$UID":"$GID" /opt/chatsubo

USER "$UID"
