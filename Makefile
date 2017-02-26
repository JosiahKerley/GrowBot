UNAME := $(shell uname)
.DEFAULT_GOAL := build


## Virtual environment
env: test-requires
	if [ ! -d env ]; then virtualenv env; fi

## Install packages needed for testing
test-requires:
	if ! virtualenv --version > /dev/null; then pip install virtualenv; fi; if ! which netstat > /dev/null; then echo missing command netstat; exit 1; fi

## Building
pkg-install: env
	. env/bin/activate; pip install https://github.com/JosiahKerley/dgi-webpowerswitch/archive/master.zip; pip install .
build: pkg-install
	bash .makescripts/build.sh

## Testing
test: env
	. env/bin/activate; cd GrowBot; python manage.py test

## Setup
setup: build
	bash .makescripts/setup.sh

## Running
run: setup stop
	. env/bin/activate; cd GrowBot; python manage.py runserver
stop: test-requires
	INSTANCE=`netstat -tulpn | awk '/8000/{print $$7}'`; if echo $${INSTANCE} | grep -E 'python'; then kill `echo $${INSTANCE} | cut -d'/' -f1`; fi

## Cleaning up
clean: stop
	rm -rf env; rm -rf nohup.out; cd GrowBot; rm -rf db.sqlite3; rm -rf growbot/migrations/*; find . -name \*.pyc -delete


## Bootstrapping
bootstrap: env
	. env/bin/activate; pip install `cat requirements.txt`; bash .makescripts/bootstrap.sh
