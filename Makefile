VIRTUALENV_FOLDER=env
PIP_BIN=$(VIRTUALENV_FOLDER)/bin/pip
PYTHON_BIN=$(VIRTUALENV_FOLDER)/bin/python


all: environment reqirements

environment:
	test -d "$(VIRTUALENV_FOLDER)" || virtualenv $(VIRTUALENV_FOLDER)

requirements:
	$(PIP_BIN) install -r requirements.txt

test: requirements
	$(PYTHON_BINARY) env/bin/django-admin.py test --settings=coupons.tests.settings

