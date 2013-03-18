TRAINING_DIR	    = /home/course/cs3245/nltk_data/corpora/reuters/training/
HOME_TRAINING_DIR   = /usr/share/nltk_data/corpora/reuters/training/
SMALL_TRAINING_DIR  = ./sample_data/

DICT_FILE	    = dict.data
POSTINGS_FILE	    = postings.data

DEV_DICT_FILE	    = dev_dict.data
DEV_POSTINGS_FILE   = dev_postings.data

QUERIES_FILE	    = queries
OUTPUT_FILE	    = output
FULL_QUERIES_FILE   = queries_full
FULL_OUTPUT_FILE    = output_full

PYTHON = python

dev: index.py
	${PYTHON} index.py -i ${SMALL_TRAINING_DIR} -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE}

query:
	${PYTHON} search.py -q ${QUERIES_FILE} -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE} -o ${OUTPUT_FILE}

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
all: dev
	@echo "all done"
build:
	rm -f *.zip
	mkdir U096857U
	git archive master | tar -x -C U096857U
	rm -rf U096857U/{sample_data,todo.org}
	cp *.data U096857U/
	cp FILE_COUNT backup_output U096857U/
	zip -r U096857U.zip U096857U
	rm -r U096857U
