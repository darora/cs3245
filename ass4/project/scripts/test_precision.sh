#! /bin/bash
OUT=tmp_output/q${1}_plot
cd ../
mkdir tmp_output
rm -f ${OUT}
echo -n "Doc-percentile " >> ${OUT}
for i in $(seq 0.05 0.05 0.95); do
    echo -n "${i} " >> ${OUT}
done
echo "" >> ${OUT}

for j in $(seq 0.05 0.05 0.95); do
    echo -n "${j} " >> ${OUT}
    for i in $(seq 0.05 0.05 0.95); do
	python2 search.py -q ./queries/q${1}.xml -d dev_dict.data -p dev_postings.data -o tmp_output/q1_o --doc-percentile ${i} --term-percentile ${j}
	# echo -n "${i} " >> ${OUT}
	python2 diff_results.py tmp_output/q1_o ./queries/q1-qrels+ve.txt >> ${OUT}
    done
    echo "" >> ${OUT}
done
    
