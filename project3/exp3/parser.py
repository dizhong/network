#!/usr/bin/env python3

# This file is used to analyze the ns2 trace files by batch

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
#import pandas as pd
import math
import sys
import json
#import numpy as np
#from pylab import cm

# first put all values into their lists?
def parse(trace, second):
    if trace == None or len(trace) < 1:
        print("trace file empty \n")
        return
        # only keep timestamp and packet# and received packet size
    q_seconds = {}
    cbrq_seconds = {}
    r_seconds = {}
    cbrr_seconds = {}
    tcp_sent = 0
    cbr_sent = 0
    for line in trace:
        split = line.split(" ")
        key = int(split[10])
        #store parameters of the traces of packets that were queued to send
        if float(split[1]) >= second:
            if split[4] == "tcp" and split[0] == "+" and split[2] == "0":
                if key in q_seconds:
                    q_seconds[key][2] += 1
                    tcp_sent += 1
                else:
                    q_seconds[key] = list((float(split[1]), int(split[5]), 1))
                    tcp_sent += 1
            #store parameters of the traces of acks that were received
            elif split[4] == "ack" and split[0] == "r" and split[3] == "0" and key in q_seconds:
                if key not in r_seconds:
                    r_seconds[key] = float(split[1])
            #sent by node 5
            elif split[4] == "cbr" and split[0] == "+" and split[2] == "4":
                if key in cbrq_seconds:
                    cbrq_seconds[key][2] += 1
                    cbr_sent += 1
                else:
                    cbrq_seconds[key] = list((float(split[1]), int(split[5]), 1))
                    cbr_sent += 1
            elif split[4] == "cbr" and split[0] == "r" and split[3] == "5":
                if key not in cbrr_seconds:
                    cbrr_seconds[key] = float(split[1])
    
    return q_seconds, r_seconds, cbrq_seconds, cbrr_seconds, tcp_sent, cbr_sent


# then calculate the averages and sums
def calculate(q_seconds, r_seconds, tcp_sent, totalSecond):
    latency_list = []
    #traffic dictionary by second
    traffic_list_temp = {0:0}
    tcp_goodput = 0
    tcp_drops = 0
    second = 0
    #print(r_seconds)
    for key in r_seconds:
        #try:
        thru_bytes = q_seconds[key][1]
        #self.traffic_raw.append(list((q_seconds[key][0],q_seconds[key][1])))
        # noting that the packet has been acked (once)
        q_seconds[key][2] -= 1
        tcp_goodput += thru_bytes
        #get the current second to add goodput bytes to
        second = int(math.floor(q_seconds[key][0]))
        if second in traffic_list_temp:
            traffic_list_temp[second] += thru_bytes
        else:
            traffic_list_temp[second] = thru_bytes
        r_time = r_seconds[key]
        q_time = q_seconds[key][0]
        latency_list.append(r_time - q_time)
    tcp_goodput_bytes = tcp_goodput
    tcp_goodput_Mbps = tcp_goodput_bytes / (125000.0 * totalSecond)
    tcp_latency = sum(latency_list) / len(latency_list)
    
    # find the number of dropped packets by counting all the packets
    # that were sent and not acked (including the retransmitted ones
    for key in q_seconds:
        tcp_drops += q_seconds[key][2]
    tcp_drop_rate = (tcp_drops / float(tcp_sent)) * 100
    # normalize the list to include 0 when there is no throughput
    for i in range(0, 125):
        if i not in traffic_list_temp:
            traffic_list_temp[i] = 0
    traffic_list = [(k,v) for k,v in sorted(traffic_list_temp.items())]
    return traffic_list, tcp_goodput_Mbps, tcp_drop_rate, tcp_latency

# main feeds files into parser, and produce graphs
def main():
    tcpV = int(sys.argv[1])
    sec = int(sys.argv[2])
    mbps = int(sys.argv[3])
    queue = int(sys.argv[4])
    fileNum = int(sys.argv[5])
    if queue == 0:
        queue = "DropTail"
    elif queue == 1:
        queue = "RED"
    else:
        print("unhandled queue #")
    if sec >= 5:
        startSec = sec
    else:
        startSec = 5
    fileName = "trace_files/exp3_" + str(fileNum) + ".tr"
    outputFile = "exp3.txt"
    outputTrace = "pngs/exp3_" + str(fileNum) + ".txt"
    file1 = open(fileName, 'r')
    lines = file1.readlines()
    q_sec, r_sec, cbrq_sec, cbrr_sec, tcp_sent, cbr_sent = parse(lines, startSec)
    traffic1_list, tcp_goodput_Mbps, tcp_drop_rate, tcp_latency = calculate(q_sec, r_sec, tcp_sent, 125-startSec)
    #print(traffic1_list)
    traffic2_list, cbr_goodput_Mbps, cbr_drop_rate, cbr_latency = calculate(cbrq_sec, cbrr_sec, cbr_sent, 125-startSec)
    xs1 = [x[0] for x in traffic1_list]
    ys1 = [x[1] for x in traffic1_list]
    ys1_mbps = [ (x / 125000.0) for x in ys1]
    xs2 = [x[0] for x in traffic2_list]
    ys2 = [x[1] for x in traffic2_list]
    ys2_mbps = [ (x / 125000.0) for x in ys2]
    plt.ylim(0, 11)
    plt.xlim(0, 130)
    plt.xlabel("Seconds")
    plt.ylabel("Mbps")
    plt.plot(xs1, ys1_mbps, '-ok', label='tcp', color='b')
    plt.plot(xs2, ys2_mbps, '-ok', label='cbr', color='y')
    plt.legend()
    plt.grid(linestyle='-', linewidth='0.5', color='grey')
    plt.savefig("pngs/exp3_" + str(fileNum) + ".png")
    plt.clf()

    file1.close()

    print(fileName)

    write_string = ("tcpV: " + str(tcpV) + "; sec:" + str(sec) + "; mbps:" \
                 " " + str(mbps) + "; counter: " + str(fileNum) + "\n" \
                 "tcp_drop_rate: " + str(tcp_drop_rate) + "%; " \
                 "tcp_goodput_Mbps: " + str(tcp_goodput_Mbps) + "; " \
                 "tcp_latency: " + str(tcp_latency) + "\n")

    print(write_string)

    output = open(outputFile, "a")
    output.write(write_string)
    output.close()

    output2 = open(outputTrace, "w")
    output2.write(write_string)
    output2.write(str(xs1) + "\n")
    output2.write(str(ys1_mbps))
    output2.close()

    json_out = open('json.txt', "a")
    data = {}
    data = {"parameters": {"tcpVersion": tcpV, 
                           "CBRStartSec": sec,
                           "CBRFlowMbps":  mbps, 
                           "Queuing": queue,
                           "SimulationCounter": fileNum},
            "results": {"tcp_drop_rate": tcp_drop_rate,
                        "tcp_goodput_Mbps": tcp_goodput_Mbps,
                        "tcp_latency": tcp_latency,
                        "cbr_drop_rate": cbr_drop_rate,
                        "cbr_goodput_Mbps": cbr_goodput_Mbps,
                        "cbr_latency": cbr_latency}
           }
    json.dump(data, json_out, indent = 4)
    json_out.write('\n')
    json_out.close()  


if __name__ == "__main__":
    main()
