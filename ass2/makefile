TRAINING_DIR = /usr/share/nltk_data/corpora/reuters/training/
SMALL_TRAINING_DIR = ./sample_data/

DICT_FILE = dict.data
POSTINGS_FILE = postings.data

dev: index.py
	python2 index.py -i ${SMALL_TRAINING_DIR} -d ${DICT_FILE} -p ${POSTINGS_FILE}

all: dev
	@echo "all done"
