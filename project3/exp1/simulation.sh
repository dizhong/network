#!/bin/sh
# counter for total script runs
counter=0
filename='exp1.txt'
jsonname='json.txt'
tracefirst='trace_files/exp1_'
tracelast='.tr'
if [ -f $filename ]; then
    rm $filename
    touch $filename
else
    touch $filename
fi
if [ -f $jsonname ]; then
    rm $jsonname
    touch $jsonname
else
    touch $jsonname
fi
# 0 = tahoe, 1 = reno, 2 = newreno, 3 = vegas
for tcpV in 0 1 2 3 
do
    # mbps in 2 4 6 8 10; iteration # * 2
    for mbps in 1 2 3 4 5 6 7 8 9 10
    do
        for tcpSec in 1 2 3 4
        do
            #for cbrSec in 1 2 3 4
            #do
            counter=$(expr $counter + 1)
            ns exp1.tcl $tcpV $mbps $tcpSec $counter
            #echo "t $counter}" >> $filename 
            python parser.py $tcpV $tcpSec $mbps $counter $filename
            tracename="$tracefirst$counter$tracelast"
            rm $tracename                 
            #done    
        done
    done
done
