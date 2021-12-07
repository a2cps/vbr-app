vbr-uninstall:
	pip uninstall -y python_vbr

vbr-install:
	pip install -r requirements.txt

vbr-update: vbr-uninstall vbr-install

deps:
	pip install -I --upgrade -r requirements.txt
	pip install -I --upgrade -r requirements-dev.txt

reformat:
	black *.py ; black tasks

lint:
	pylint --enable=F,E --disable=W,C,R *.py tasks/*.py

isort:
	isort *.py

image:
	docker build -t a2cps/vbr_api .

build_ecr: image
	docker tag a2cps/vbr_api:latest 673872715994.dkr.ecr.us-east-1.amazonaws.com/a2cps/vbr_api:latest

deploy: build_ecr
	docker push 673872715994.dkr.ecr.us-east-1.amazonaws.com/a2cps/vbr_api:latest

localhost:
	uvicorn application.main:app --reload
