TAG_COMMIT := $(shell git rev-list --abbrev-commit --tags --max-count=1)
COMMIT := $(shell git rev-parse --short HEAD)
DATE := $(shell git log -1 --format=%cd --date=format:"%Y%m%d")
VERSION := $(COMMIT)-$(DATE)

vbr-uninstall:
	pip uninstall -y python_vbr

vbr-install:
	pip install -r requirements.txt

vbr-update: vbr-uninstall vbr-install

deps:
	pip install -I --upgrade -r requirements.txt
	pip install -I --upgrade -r requirements-dev.txt

reformat:
	black *.py

lint:
	pylint --enable=F,E --disable=W,C,R application

isort:
	isort *.py

image:
	docker build --build-arg BUILD_VERSION=$(VERSION) --no-cache -t a2cps/vbr_api .

build_ecr: image
	docker tag a2cps/vbr_api:latest 673872715994.dkr.ecr.us-east-1.amazonaws.com/a2cps/vbr_api:latest

auth_ecr:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 673872715994.dkr.ecr.us-east-1.amazonaws.com

deploy: build_ecr auth_ecr
	docker push 673872715994.dkr.ecr.us-east-1.amazonaws.com/a2cps/vbr_api:latest

localhost:
	uvicorn application.main:app --reload

compose-up:
	docker-compose up --build --force-recreate -d

compose-down:
	docker-compose down

.PHONY: docs
docs:
	cd docs; make html
