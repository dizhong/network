#!/bin/bash

for runs in 1 2 3 4 5
do
	sudo ./rawhttpget https://david.choffnes.com/classes/cs4700fa20/2MB.log
	echo $runs
done
