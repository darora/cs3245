from itertools import imap
import sys, string

if len(sys.argv) != 3:
    print "Usage: diff_results.py [YOUR_RESULTS] [REFERENCE_RESULTS]"
    raise Exception("Need two files to diff")

def read_in(fl_name):
    with open(fl_name, 'r') as fl:
        text = fl.readlines()
        text = map(string.strip, text)
        text = set(text)
        return text

def get_diff(seta, setb):
    diff = seta - setb
    to_print = '\n'.join(diff)
    return str(len(diff)), to_print

fl_1 = read_in(sys.argv[1])
fl_2 = read_in(sys.argv[2])

dmiss = get_diff(fl_2, fl_1)
dwrong = get_diff(fl_1, fl_2)

print dmiss[0] + " documents were missed!"
print dmiss[1]

print dwrong[0] + " documents were WRONG!"
# print dwrong[1]
