.PHONY: build default

default: help

## prod: Build project and start the server
prod: build gunicorn

## build : Build front end
build:
	npm --prefix=front/ run build

## install_full : Create virtualenv and install node and python dependencies
install_full: venv install

## install: Install node and python dependencies
install: install_node install_pip

## gunicorn : Start gunicorn on port 5000
gunicorn:
	./venv/bin/gunicorn -k eventlet app:server -w 1 --log-file - --bind 0.0.0.0:5000

## celery : Start the celery server
celery:
	./venv/bin/celery -A app.queue worker --concurrency 5 -l INFO

## flask : Start flask dev env
flask:
	./venv/bin/python run.py

## vue : Start Vue dev env
vue:
	npm --prefix=front/ run serve

## venv : Create virtualenv
venv:
	python3 -m virtualenv venv --python=`which python3`

## install_node : Install nodes_modules
install_node:
	npm --prefix=front/ i

## install_pip : Install pip packages
install_pip:
	./venv/bin/pip install -r ./requirements.txt

## docker : Build and start docker compose
docker:
	docker-compose up --build -d

## docker_build : Build docker compose
docker_build:
	docker-compose up --build

## docker_start : Start docker compose
docker_start:
	docker-compose up -d

## req : Freeze pyhton requirements
req:
	./venv/bin/pip freeze | grep -v "pkg-resources" > requirements.txt

## help : This help
help: Makefile
		@printf "\n Chatsubo : pwn stuff\n\n"
		@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
		@printf ""
