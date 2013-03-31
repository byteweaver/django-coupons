VIRTUALENV_FOLDER=env
PIP_BIN=$(VIRTUALENV_FOLDER)/bin/pip
PYTHON_BIN=$(VIRTUALENV_FOLDER)/bin/python


all: environment reqirements

environment:
	test -d "$(VIRTUALENV_FOLDER)" || virtualenv --no-site-packages $(VIRTUALENV_FOLDER)

reqirements:
	$(PIP_BIN) install -r requirements.txt

test:
	$(PYTHON_BIN) coupons/tests/runtests.py

