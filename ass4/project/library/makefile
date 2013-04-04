PYTHON ?= python
CUR_PATH = $(shell echo $$PYTHONPATH)
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON} --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
LIB_PATH ?= ${CWD}/built/lib/python${python_version_major}.${python_version_minor}/site-packages/
export PYTHONPATH = ${CUR_PATH}:${CWD}/built/lib/python${python_version_major}.${python_version_minor}/site-packages/
CWD = $(shell pwd)

distribute:
	tar -xzf distribute.tar.gz
	cd distribute && ${PYTHON} setup.py install --prefix=${CWD}/built
	rm -rf distribute

blist:
	tar -xzf blist.tar.gz
	cd blist && ${PYTHON} setup.py install --prefix=${CWD}/built
	rm -rf blist

all: create_dir distribute blist

create_dir:
	mkdir -p ${LIB_PATH}

.PHONY: all blist distribute create_dir
