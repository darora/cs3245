set autoscale
set term post
set out "outfile_1.png"
unset logscale
unset label
set xtic auto
set ytic auto
set title "Precision against doc/term cutoff percentiles"
set xlabel "Percentile"
set ylabel "Precision"
set grid
set key autotitle columnhead
plot for [i=1:100] '../tmp_output/q1_plot' using 1:i  with linespoints
# plot "../tmp_output/q1_plot" using 1:2 title 'Mean power' with linespoints
set yrange [0:0.05]
set out "outfile_2.png"
plot for [i=1:100] '../tmp_output/q2_plot' using 1:i  with linespoints