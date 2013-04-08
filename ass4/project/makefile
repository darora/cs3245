SMALL_TRAINING_DIR  = ./corpus/

DEV_DICT_FILE	    = dev_dict.data
DEV_POSTINGS_FILE   = dev_postings.data

PYTHON = python2
CUR_PATH = $(shell echo $$PYTHONPATH)
CWD = $(shell pwd)
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON} --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
LIB_PATH = ${CWD}/built/lib/python${python_version_major}.${python_version_minor}/site-packages/
export PYTHONPATH = ${CUR_PATH}:${CWD}/library/built/lib/python${python_version_major}.${python_version_minor}/site-packages/

.PHONY: library dev query gui clean

clean:
	rm -f dev_dict.data dev_postings.data output_1 output_2
gui:
	${PYTHON} render_data.py

diff: diff_1 diff_2

diff_1:	output_1 dev_dict.data dev_postings.data
	@echo "########## First query, positive."
	${PYTHON} diff_results.py output_1 ./queries/q1-qrels+ve.txt --verbose
diff_2: output_2 dev_dict.data dev_postings.data
	@echo "########## Second query, positive."
	${PYTHON} diff_results.py output_2 ./queries/q2-qrels+ve.txt --verbose

library:
	cd library && make all
dir:
	if test ! -d processed; then mkdir processed; fi
dev: indexer.py index.py dir dev_postings.data dev_dict.data

dev_postings.data dev_dict.data: index.py indexer_targets.py utils.py
	${PYTHON} index.py -i ${SMALL_TRAINING_DIR} -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE}
output_1: search.py dev_dict.data dev_postings.data .FORCE
	${PYTHON} search.py -q ./queries/q1.xml -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE} -o $@
output_2: search.py dev_dict.data dev_postings.data .FORCE
	${PYTHON} search.py -q ./queries/q2.xml -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE} -o $@
.FORCE:

query: output_1 output_2

test: .FORCE
	cd scripts && ./test_precision.sh 1 && ./test_precision.sh 2
	cd scripts && gnuplot plot_results.gp

build:
	rm -f *.zip
	mkdir U096857U
	git archive master | tar -x -C U096857U
	rm -rf U096857U/{sample_data,todo.org,corpus,processed,queries,library}
	zip -r U096857U.zip U096857U
	rm -r U096857U

build2:
	rm -f *.zip
	mkdir U0906857
	git archive master | tar -x -C U0906857
	rm -rf U0906857/{sample_data,todo.org,corpus,processed,queries,library}
	zip -r U0906857.zip U0906857
	rm -r U0906857
