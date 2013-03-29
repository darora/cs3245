#!/usr/bin/python2

import commands

def calc(fd):
    fl_count = 0
    fl_length = 0
    for line in fd.readlines():
        fls = line.strip().split()
        for fl in fls:
            fl_count += 1
            o = commands.getstatusoutput('wc -l /usr/share/nltk_data/corpora/reuters/training/'+fl)
            fl_length += int(o[1].split()[0])
    return fl_length/fl_count
    




new_o = open('output', 'r')
ave = calc(new_o)
print "New average length is "+str(ave)
new_o.close()




fl_count = 0
fl_length = 0

new_o = open('backup_output', 'r')
ave = calc(new_o)
print "Old average length is "+str(ave)
new_o.close()
