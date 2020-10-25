#!/bin/sh
# counter for total script runs
counter=0
filename='exp2.txt'
jsonname='json.txt'
tracefirst='trace_files/exp2_'
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
# 0 = reno/reno, 1 = newreno/reno, 2 = vegas/vegas, 3 = newreno/vegas
for tcpV in 0 1 2 3 
do
    # mbps in 2 4 6 8 10; iteration # * 2
    for mbps in 2 4 6 8 10
    do
        for sec in 1 2 3 4
        do
            counter=$(expr $counter + 1)
            ns exp1.tcl $tcpV $mbps $sec $counter
            #echo "t $counter}" >> $filename 
            python parser.py $tcpV $sec $mbps $counter $filename
            tracename="$tracefirst$counter$tracelast"
            rm $tracename                 
                
        done
    done
done
