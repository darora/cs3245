TRAINING_DIR	    = /usr/share/nltk_data/corpora/reuters/training/
SMALL_TRAINING_DIR  = ./sample_data/

DICT_FILE	    = dict.data
POSTINGS_FILE	    = postings.data

DEV_DICT_FILE	    = dev_dict.data
DEV_POSTINGS_FILE   = dev_postings.data

QUERIES_FILE	    = queries
OUTPUT_FILE	    = output

PYTHON = /usr/bin/python2

dev: index.py
	${PYTHON} index.py -i ${SMALL_TRAINING_DIR} -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE}

query:
	${PYTHON} search.py -q ${QUERIES_FILE} -d ${DEV_DICT_FILE} -p ${DEV_POSTINGS_FILE} -o ${OUTPUT_FILE}

test:
	@echo "Running unit tests..."
	${PYTHON} tests.py

build_full_index:
	${PYTHON} index.py -i ${TRAINING_DIR} -d ${DICT_FILE} -p ${POSTINGS_FILE}

all: dev
	@echo "all done"
