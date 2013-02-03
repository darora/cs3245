#!/usr/bin/env python2
#TODO::revert to /usr/bin/python

import string
import re
import nltk
import sys
import getopt
import math
import pickle
from collections import defaultdict

models = {}
pristine_models = {}
languages = ["indonesian", "malaysian", "tamil"]
counter_label = "counter"
NGRAM_LENGTH = 5

def initialize_shits():
    """
    Using a defaultdict here takes care of smoothing "by default"
    """
    for lang in languages:
        models[lang] = defaultdict(lambda: 1)
        models[lang][counter_label] = 0
        
def pad_string(str, char="\0"):
    """
    Pads strings for the creation of 4-grams with a default null char.
    Returns padded string.
    """
    return "{s:{c}^{n}}".format(s=str.strip(), c=char, n=len(str)+2*(NGRAM_LENGTH-1))

def preprocess_line(line, strip_NNP=True):
    """
    * If strip_NNP is True, it strips out Proper Nouns from the line, since it is assumed that these don't have much specificity to the language being considered (especially since we'll be detecting "English" nouns)
    * Converts resultant string to lowercase and returns it.
    """
    if strip_NNP == True:
        txt = nltk.word_tokenize(line)
        tagged_txt = nltk.pos_tag(txt)
        nnp = [word for (word, pos) in tagged_txt if pos == "NNP"]
        for word in nnp:
            line = line.replace(word, "")
        # Multiple replacements can cause multiple spaces, so replace them with just the one.
        line = re.sub(r'\s+', ' ', line)
    return line
# TODO::add tokens to other langs
def explode_line(line, lang):
    """
    I use strings as indices, rather than tuples as shown in the pdf, for performance. In very naive, simplistic testing, strings seemed to be ~25ns faster per dict operation.
    Arguments:
    - `line`: a preprocessed, padded line.
    - `lang`: the language the string is in.(indonesian|malaysian|tamil)
    """
    tokens = nltk.word_tokenize(line)
    for token in tokens:
        models[lang][token] += 1
        models[lang][counter_label] += 1
    
def postprocess_counts():
    """
    Converts all the counts into log(probabilities)
    """
    pristine_models = models.copy()
    # for lang in languages:
    #     model = models[lang]
    #     total = model[counter_label]
    #     new_default = math.log10(1.0/total)
    #     model.default_factory = lambda: new_default
    #     for word in model.keys():
    #         if word == counter_label:
    #             continue
    #         else:
    #             model[word] = math.log10(float(model[word])/total)

def increment_token_count(model, token):
    model[token] += 1
    model[counter_label] += 1
    
def get_likely_langauge(test_string):
    processed_str = pad_string(preprocess_line(test_string))
    selected_lang = ""
    selected_lang_prob = -sys.maxint - 1

    models = pristine_models.copy()

    # first pass, add in terms that aren't already in the LM, and
    # calculate probabilities appropriately
    for lang in models.keys():
        model = models[lang]
        for token in tokens:
            if token in model:
                continue
            else:
                increment_token_count(model, token)
        total = model[counter_label]
        for word in model.keys():
            model[word] = math.log10(float(model[word])/total)
        
    for lang in languages:
        model = models[lang].copy()
        current_prob = 0.0
        tokens = nltk.word_tokenize(processed_str)
        for token in tokens:
            # if token in model:
            #     pass
            # else:
            #     pass
            current_prob += model[token]
        if current_prob > selected_lang_prob:
            selected_lang_prob = current_prob
            selected_lang = lang
    return (selected_lang, selected_lang_prob)

def store_LM():
    dump_file = open("models", "wb")
    pickle.dump(models, dump_file, 2)
    dump_file.close()
    
def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    initialize_shits()
        
    print 'building language models...'    
    split_regex = re.compile(r'(\w+) (.*)')
    for line in open(in_file):
        matches = split_regex.match(line)
        lang = matches.group(1)
        line = matches.group(2)
        line = preprocess_line(line, True)
        line = pad_string(line)
        explode_line(line, lang)
    postprocess_counts()
    #store_LM()
    print 'done building models'
    
    # This is an empty method
    # Pls implement your code in below
    
def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    output = open(out_file, 'w')
    for line in open(in_file):
        vl = get_likely_langauge(line)
        output.write(vl[0] + " " + line)
        print vl
    output.close()
    
    # This is an empty method
    # Pls implement your code in below

def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    # TODO::sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
