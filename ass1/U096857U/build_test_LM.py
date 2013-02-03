#!/usr/bin/env python2
#TODO::revert to /usr/bin/python

import string
import re
import copy
import nltk
import sys
import getopt
import math
import pickle
from collections import defaultdict

models = {}
pristine_models = {}
languages = ["indonesian", "malaysian", "tamil"]
counter_label = "counter"       # this is used to maintain the total
# count for each language

# globals that are populated by optional CLI parameters
g_lowercase = False
g_strip_NNP = False
g_tokenize = False
g_char_length = 4

def initialize_models():
    """
    Initializes data structs for each lang.
    Using a defaultdict here takes care of smoothing "by default"
    """
    for lang in languages:
        models[lang] = defaultdict(lambda: 1)
        models[lang][counter_label] = 0
        
def pad_string(line, char="\0"):
    """
    Pads strings for the creation of n-grams with a default null char.
    Affected by g_char_length: pads (n-1) chars on each side
    
    Returns padded string.
    """
    return "{s:{c}^{n}}".format(s=line.strip(), c=char, n=len(line) + 2*(g_char_length-1))

def preprocess_line(line):
    """
    * If g_strip_NNP is True, it strips out Proper Nouns from the line
    * If g_lowercase is True, converts resultant string to lowercase
    
    returns string
    """
    if g_strip_NNP == True:
        txt = nltk.word_tokenize(line)
        tagged_txt = nltk.pos_tag(txt)
        nnp = [word for (word, pos) in tagged_txt if pos == "NNP"]
        for word in nnp:
            line = line.replace(word, "")
        # Multiple replacements can cause multiple spaces, so replace them with just the one.
        line = re.sub(r'\s+', ' ', line)

    # Temp test if removing punctuation/digits helps
    # regexp = re.compile("[" + re.escape(string.punctuation + string.digits) +"]")
    # line = regexp.sub("", line)
        
    if g_lowercase == True:
        line = line.lower()
    return line

def tokenize_line(line):
    """
    Expects a preprocessed line
    Affected by:
    * g_char_length
    * g_tokenize

    Returns a list of tokens--either nltk tokens, or n-grams.
    """
    if g_tokenize:
        return nltk.word_tokenize(line)
    else:
        return [line[i:i+g_char_length] for i in range(len(line) - g_char_length - 1)]

def increment_token_count(model, token):
    """
    Standardized method for incrementing the count of a token for a particular LM.
    """
    model[token] += 1
    model[counter_label] += 1

def process_line(line, lang):
    """
    Breaks the line apart into tokens as necessary, and adds them to the LM.
    
    I use strings as indices, rather than tuples as shown in the pdf, for performance. In very naive, simplistic testing, strings seemed to be ~25ns faster per dict operation.
    
    Arguments:
    - `line`: a preprocessed, padded line.
    - `lang`: the language the string is in.(indonesian|malaysian|tamil)
    """
    tokens = tokenize_line(line)
    
    for token in tokens:
        increment_token_count(models[lang], token)
    
def postprocess_counts():
    """
    Remnants of a legacy method.
    Just assigns a copy of the trained LMs to ``pristine_models''

    pristine_models will be used to create a fresh copy of each LM for each string that we attempt to identify.
    """
    global pristine_models
    pristine_models = models
    
def get_likely_langauge(test_string):
    """
    Runs the test string through the usual gamut of preprocessing, padding, tokenization etc.

    Makes two-passes over the string for each LM. Comments included inline.

    Returns a tuple of (predicted language, confidence)
    """
    processed_str = pad_string(preprocess_line(test_string))
    selected_lang = ""
    selected_lang_prob = -sys.maxint - 1

    models = copy.deepcopy(pristine_models) # Obtain a fresh copy.
    # We'll add unseen terms to this copy, so that they don't taint our LM
    # for future strings

    for lang in languages:
        model = models[lang]
        tokens = tokenize_line(processed_str)
        current_prob = 0.0
        
        # first pass, add in terms that aren't already in the LM
        for token in tokens:
            if token in model:
                continue
            else:
                increment_token_count(model, token)
        total = model[counter_label]
        
        # calculate probabilities & store their log values.
        for word in model.keys():
            model[word] = math.log10(float(model[word])/total)

        # second pass, calculate likelihood of the string being from
        # this language
        for token in tokens:
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
    initialize_models()
        
    print 'building language models...'    
    split_regex = re.compile(r'(\w+) (.*)')
    for line in open(in_file):
        matches = split_regex.match(line)
        lang = matches.group(1)
        line = matches.group(2)
        line = preprocess_line(line)
        line = pad_string(line)
        process_line(line, lang)
    postprocess_counts()
    print 'done building models'
    
    
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
        # print vl
    output.close()
    
def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file [--lowercase True] [--strip-NNP True] [--tokenize True] [--char-length N]"


def str2bool(v):
  return v.lower() in ("true", "yes")
    
input_file_b = input_file_t = output_file = None

for index, arg in enumerate(sys.argv[1:]):
    if arg == '-b':
        input_file_b = sys.argv[1+1+index]
    elif arg == '-t':
        input_file_t = sys.argv[1+1+index]
    elif arg == '-o':
        output_file = sys.argv[1+1+index]
    elif arg == '--lowercase':
        g_lowercase = str2bool(sys.argv[1+1+index])
    elif arg == '--strip-NNP':
        g_strip_NNP = str2bool(sys.argv[1+1+index])
    elif arg == '--tokenize':
        g_tokenize = str2bool(sys.argv[1+1+index])
    elif arg == '--char-length':
        g_char_length = int(sys.argv[1+1+index])
        
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
