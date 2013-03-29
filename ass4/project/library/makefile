PYTHON ?= python2
CUR_PATH = $(shell echo $$PYTHONPATH)
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON} --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
export PYTHONPATH ?= ${CUR_PATH}:${CWD}/built/lib/python${python_version_major}.${python_version_minor}/site-packages/
CWD = $(shell pwd)

distribute:
	tar -xzf distribute.tar.gz
	cd distribute && python2 setup.py install --prefix=${CWD}/built
	rm -rf distribute

blist:
	tar -xzf blist.tar.gz
	cd blist && python2 setup.py install --prefix=${CWD}/built
	rm -rf blist

all: distribute blist

.PHONY: all blist distribute
