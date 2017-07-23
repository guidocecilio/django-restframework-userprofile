PYTHON=python2.7
ENV_DIR=.env
STATIC_DIR=clients/cm_webapp

ifndef DJANGO_DB
    DJANGO_DB=db.sqlite
endif
PROJECT_NAME=public_profile
DJANGO_MANAGE=scripts/manage.py

WITH_DEFAULT_SETTINGS=export DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).settings &&
WITH_TEST_SETTINGS=export DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).settings &&
WITH_CONTEXT=export DJANGO_SQLITE_PATH=$(DJANGO_DB) && $(WITH_DEFAULT_SETTINGS)

ifndef DEV_PORT
    DEV_PORT=8000
endif

ifeq ($(OS),Windows_NT)
	IN_ENV=. $(ENV_DIR)/Scripts/activate &&
else
	IN_ENV=. $(ENV_DIR)/bin/activate &&
endif

all: test lint docs artifacts

env: $(ENV_DIR)

test: build
	$(IN_ENV) $(WITH_CONTEXT) coverage run $(DJANGO_MANAGE) test
	$(IN_ENV) $(WITH_CONTEXT) coverage combine
	$(IN_ENV) $(WITH_CONTEXT) coverage xml -i
	$(IN_ENV) $(WITH_CONTEXT) coverage report -m

artifacts: build_reqs rpm sdist

$(ENV_DIR):
	virtualenv -p $(PYTHON) $(ENV_DIR)

npm:
	cd $(STATIC_DIR) && npm run build

build_reqs: env
	$(IN_ENV) pip install herodotus sphinx pep8 coverage nose
	$(IN_ENV) pip install -r requirements.txt

build: build_reqs npm
	$(IN_ENV) pip install --editable .

build_service: build_reqs
	$(IN_ENV) pip install --editable .

sdist: build_reqs
	$(IN_ENV) python setup.py sdist

rpm: build_reqs
	$(IN_ENV) rpmbuild --define 'dist .el7' --define '_topdir '`pwd` -bb SPECS/*.spec

lint: pep8

pep8: build_reqs
	- $(IN_ENV) pep8 src | tee pep8.out

flake8: build_reqs
	- $(IN_ENV) flake8 src | tee flake8.out

docs: build_reqs
	$(IN_ENV) pip install -r docs/requirements.txt
	$(IN_ENV) $(MAKE) -C docs html

db.sqlite:
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) syncdb --noinput

superuser: db.sqlite
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) createsuperuser

#serve: build
#	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) syncdb --noinput
#	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) runserver

serve:
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) runserver

serve-all:
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) runserver 0:$(DEV_PORT)

migrate: db.sqlite
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) migrate

migrations: db.sqlite
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) makemigrations

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
