VIRTUALENV_FOLDER=env
PIP_BIN=$(VIRTUALENV_FOLDER)/bin/pip
PYTHON_BIN=$(VIRTUALENV_FOLDER)/bin/python
COVERAGE_BINARY=$(VIRTUALENV_FOLDER)/bin/coverage

all: test

environment:
	test -d "$(VIRTUALENV_FOLDER)" || virtualenv $(VIRTUALENV_FOLDER)

requirements: environment
	$(PIP_BIN) install -r requirements.txt

test: requirements
	$(PYTHON_BINARY) env/bin/django-admin.py test --settings=coupons.tests.settings

coverage: requirements
		$(COVERAGE_BINARY) erase
		$(COVERAGE_BINARY) run --branch --source=coupons env/bin/django-admin.py test --settings=coupons.tests.settings
		$(COVERAGE_BINARY) html
