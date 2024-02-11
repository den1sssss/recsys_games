PYTHON ?= .venv/bin/python
PYTHON_PRE ?= ../.venv/bin/python

install:
	python3.10 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt

jup:
	$(PYTHON) -m jupyterlab

jup-darwin:
	$(PYTHON) -m jupyterlab --app-dir=/opt/homebrew/share/jupyter/lab

train:
	cd src && $(PYTHON_PRE) -m rasa train

run:
	LOGURU_LEVEL=DEBUG cd src && $(PYTHON_PRE) -m rasa run actions

shell:
	cd src && $(PYTHON_PRE) -m rasa shell

help:
	cd src && $(PYTHON_PRE) -m rasa

test:
	cd src && $(PYTHON_PRE) -m pytest -s
