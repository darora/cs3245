TRAINING_DIR	    = /usr/share/nltk_data/corpora/reuters/training/
SMALL_TRAINING_DIR  = ./sample_data/

DICT_FILE	    = dict.data
POSTINGS_FILE	    = postings.data

QUERIES_FILE	    = queries
OUTPUT_FILE	    = output

PYTHON = /usr/bin/python2

dev: index.py
	${PYTHON} index.py -i ${SMALL_TRAINING_DIR} -d ${DICT_FILE} -p ${POSTINGS_FILE}

query:
	${PYTHON} search.py -q ${QUERIES_FILE} -d ${DICT_FILE} -p ${POSTINGS_FILE} -o ${OUTPUT_FILE}

test:
	@echo "Running unit tests..."
	${PYTHON} tests.py

all: dev
	@echo "all done"
