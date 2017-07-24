PYTHON=python2.7
ENV_DIR=.env
STATIC_DIR=clients

ifndef DJANGO_DB
    DJANGO_DB=db.sqlite
endif
PROJECT_NAME=public_profile
DJANGO_MANAGE=src/manage.py

WITH_DEFAULT_SETTINGS=export DJANGO_SETTINGS_MODULE=public_profile.settings &&
WITH_TEST_SETTINGS=export DJANGO_SETTINGS_MODULE=public_profile.settings &&
WITH_CONTEXT=export DJANGO_SQLITE_PATH=$(DJANGO_DB) && $(WITH_DEFAULT_SETTINGS)

ifndef DEV_PORT
    DEV_PORT=8000
endif

ifeq ($(OS),Windows_NT)
	IN_ENV=. $(ENV_DIR)/Scripts/activate &&
else
	IN_ENV=. $(ENV_DIR)/bin/activate &&
endif

all: test lint artifacts

env: $(ENV_DIR)

test:
	$(IN_ENV) $(WITH_CONTEXT) coverage run $(DJANGO_MANAGE) test
	$(IN_ENV) $(WITH_CONTEXT) coverage combine
	$(IN_ENV) $(WITH_CONTEXT) coverage xml -i
	$(IN_ENV) $(WITH_CONTEXT) coverage report -m

artifacts: build_reqs sdist

$(ENV_DIR):
	virtualenv -p $(PYTHON) $(ENV_DIR)

build_reqs: env
	$(IN_ENV) pip install herodotus sphinx pep8 coverage nose
	$(IN_ENV) pip install -r requirements.txt

sdist: build_reqs
	$(IN_ENV) python setup.py sdist

lint: pep8

pep8: build_reqs
	- $(IN_ENV) pep8 src | tee pep8.out

flake8: build_reqs
	- $(IN_ENV) flake8 src | tee flake8.out

migrate:
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) migrate

migrations: db.sqlite
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) makemigrations

fixtures: migrate
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) loaddata src/api/fixtures/*

superuser:
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) createsuperuser

serve:
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) runserver

clean:
	- @rm -rf BUILD
	- @rm -rf BUILDROOT
	- @rm -rf RPMS
	- @rm -rf SRPMS
	- @rm -rf SOURCES
	- @rm -rf docs/build
	- @rm -rf src/*.egg-info
	- @rm -rf build
	- @rm -rf dist
	- @rm -f .coverage
	- @rm -f test_results.xml
	- @rm -f coverage.xml
	- @rm -f pep8.out
	- @find ./src ./docs -name '*.pyc' | xargs -r rm

env_clean: clean
	- @rm -rf $(ENV_DIR)

clean_all: clean env_clean
	- @rm *.sqlite
