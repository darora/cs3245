#!/usr/bin/env python2
options = [("lowercase", [True, False]), ("strip-NNP", [True, False]), ("tokenize", [True, False]), ("char-length", [1,2,3,4,5])]

f = open("makefile", "w")

f.write("# generated from gen_makefile.py")
f.write("# changes will be overwritten!"+'\n')

for index, lwr in enumerate(options[0][1]):     # lowercase or not
    if index == 0:
        opt = "first"
        f.write(opt+":\n")
    else:
        opt = "second"
        f.write(opt+":\n")
    for strip in options[1][1]:
        for clen in options[3][1]:
            for token in options[2][1]:
                name = "lower_{lower}_strip_{strip}_token_{token}_charLen_{clen}.output".format(lower=str(lwr), strip = str(strip), token = str(token), clen = str(clen))
                f.write("\t@echo \"starting on the config: {conf}\" \n".format(conf = name))
                string = "\tpython build_test_LM.py -b input.train.txt -t input.test.txt -o {name} --lowercase {lower} --strip-NNP {strip} --tokenize {token} --char-length {clen} | tee {name}_prob".format(lower=str(lwr), strip = str(strip), token = str(token), clen = str(clen), name=name)
                f.write(string + '\n')
                f.write("\techo \"" + name + "\" >> output_counts."+ opt + '\n')
                diff_count = "\tdiff {name} input.correct.txt | /usr/xpg4/bin/grep -E '^>' | wc -l | tee -a output_counts.{opt}\n".format(name=name, opt=opt)
                f.write(diff_count)

clean = """
clean:
	rm -f output_counts.first
	rm -f output_counts.second
"""

compile = """
compile:
	rm -f output_counts
	cat output_counts.first output_counts.second > output_counts
"""

f.write(clean)
f.write(compile)

f.close()

