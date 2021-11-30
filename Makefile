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
