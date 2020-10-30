#!/bin/sh
# counter for total script runs
counter=0
filename='exp3.txt'
jsonname='json.txt'
tracefirst='trace_files/exp3_'
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
# 0 = reno, 1 = SACK
for tcpV in 0 1 
do
    # mbps in 2 4 6 8 10; iteration # * 2
    for mbps in 5
    do
        for sec in 20 25 30 35 40 45 50 55
        do
            for queue in 0 1
            do
                counter=$(expr $counter + 1)
                ns exp3.tcl $tcpV $mbps $sec $queue $counter
                #echo "t $counter}" >> $filename 
                python parser.py $tcpV $sec $mbps $queue $counter $filename
                tracename="$tracefirst$counter$tracelast"
                rm $tracename                 
            done    
        done
    done
done
