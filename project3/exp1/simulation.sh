#!/bin/sh
# counter for total script runs
counter=0
# 0 = tahoe, 1 = reno, 2 = newreno, 3 = vegas
for tcpV in 0 
do
    # tcp start at 5 sec; cbr start at 1, 5, 10, 15 sec
    for sec in 1 5 10 15
    do
        # mbps in 2 4 6 8 10; iteration # * 2
        for mbps in 2 4 6 8 10
        do
            for repeat in 1 2 3 4 5 6 7 8 9 10
            do
                counter=$(expr $counter + 1)
                ns exp1.tcl $tcpV $sec $mbps $counter
            done
        done
    done
done
