TRAINING_DIR	    = /home/course/cs3245/nltk_data/corpora/reuters/training/
HOME_TRAINING_DIR   = /usr/share/nltk_data/corpora/reuters/training/
SMALL_TRAINING_DIR  = ./corpus/

DICT_FILE	    = dict.data
POSTINGS_FILE	    = postings.data

DEV_DICT_FILE	    = dev_dict.data
DEV_POSTINGS_FILE   = dev_postings.data

QUERIES_FILE	    = queries
OUTPUT_FILE	    = output
FULL_QUERIES_FILE   = queries_full
FULL_OUTPUT_FILE    = output_full

PYTHON = python
CUR_PATH = $(shell echo $$PYTHONPATH)
CWD = $(shell pwd)
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON} --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
LIB_PATH = ${CWD}/built/lib/python${python_version_major}.${python_version_minor}/site-packages/
export PYTHONPATH = ${CUR_PATH}:${CWD}/library/built/lib/python${python_version_major}.${python_version_minor}/site-packages/

.PHONY: library dev query test build_full_index full_query gui

gui:
	${PYTHON} render_data.py

diff: diff_1 diff_2

diff_1:	output_1
	@echo "First query, negative. Whatever that means."
	${PYTHON} diff_results.py output_1 ./queries/q1-qrels-ve.txt
	@echo "First query, positive."
	${PYTHON} diff_results.py output_1 ./queries/q1-qrels+ve.txt
diff_2: output_2
	@echo "Second query, negative. Whatever that means."
	${PYTHON} diff_results.py output_2 ./queries/q2-qrels-ve.txt
	@echo "Second query, positive."
	${PYTHON} diff_results.py output_2 ./queries/q2-qrels+ve.txt

library:
	cd library && make all
dir:
	if test ! -d processed; then mkdir processed; fi
dev: dir
	echo $$PYTHONPATH
	${PYTHON} index.py -i ${SMALL_TRAINING_DIR} -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE}

output_1: search.py
	${PYTHON} search.py -q ./queries/q1.xml -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE} -o $@
output_2: search.py
	${PYTHON} search.py -q ./queries/q2.xml -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE} -o $@
query: output_1 output_2

test:
	@echo "Running unit tests..."
	${PYTHON} tests.py
	make full_query
	@echo "Difference in the outputs for the sample set of queries--"
	diff output backup_output

build_full_index: index.py
	${PYTHON} index.py -i ${TRAINING_DIR} -d ${DICT_FILE} -p ${POSTINGS_FILE}

h_build_full_index: index.py
	${PYTHON} index.py -i ${HOME_TRAINING_DIR} -d ${DICT_FILE} -p ${POSTINGS_FILE}

full_query:
	${PYTHON} search.py -q ${FULL_QUERIES_FILE} -d ${DICT_FILE} -p ${POSTINGS_FILE} -o ${OUTPUT_FILE}

check: full_query
	diff sample_output output
build:
	rm -f *.zip
	mkdir U096857U
	git archive master | tar -x -C U096857U
	rm -rf U096857U/{sample_data,todo.org}
	cp *.data U096857U/
	cp FILE_COUNT backup_output U096857U/
	zip -r U096857U.zip U096857U
	rm -r U096857U
