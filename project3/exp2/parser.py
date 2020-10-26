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

# The Parser class processes the individual trace files
#class Parser:
#    def __init__(self, trace_list):
#        self.trace = trace_list
#
#        self.tcp1_goodput_bytes = 0.0
#        self.tcp1_goodput_Mbps = 0.0
#        self.tcp1_latency = None
#        self.tcp1_drops = 0
#        self.tcp1_sent = 0
#        self.traffic1_list = []
#        self.traffic1_raw = []
#
#        self.tcp1_goodput_bytes = 0.0
#        self.tcp1_goodput_Mbps = 0.0
#        self.tcp1_latency = None
#        self.tcp1_drops = 0
#        self.tcp1_sent = 0
#        self.traffic1_list = []
#        self.traffic1_raw = []


    # first put all values into their lists?
def parse(trace):
    if trace == None or len(trace) < 1:
        print("trace file empty \n")
        return
        # only keep timestamp and packet# and received packet size
    q1_seconds = {}
    q2_seconds = {}
    r1_seconds = {}
    r2_seconds = {}
    tcp1_sent = 0
    tcp2_sent = 0
    for line in trace:
        split = line.split(" ")
        key = int(split[10])
        #store parameters of the traces of packets that were queued to send
        if split[4] == "tcp" and split[0] == "+" and split[2] == "0":
            if key in q1_seconds:
                q1_seconds[key][2] += 1
                tcp1_sent += 1
            else:
                q1_seconds[key] = list((float(split[1]), int(split[5]), 1))
                tcp1_sent += 1
        #store parameters of the traces of acks that were received
        elif split[4] == "ack" and split[0] == "r" and split[3] == "0":
            if key not in r1_seconds:
                r1_seconds[key] = float(split[1])
        #sent by node 5
        elif split[4] == "tcp" and split[0] == "+" and split[2] == "4":
            if key in q2_seconds:
                q2_seconds[key][2] += 1
                tcp2_sent += 1
            else:
                q2_seconds[key] = list((float(split[1]), int(split[5]), 1))
                tcp2_sent += 1
        elif split[4] == "ack" and split[0] == "r" and split[3] == "4":
            if key not in r2_seconds:
                r2_seconds[key] = float(split[1])
    return q1_seconds, r1_seconds, q2_seconds, r2_seconds, tcp1_sent, tcp2_sent


# then calculate the averages and sums
def calculate(q_seconds, r_seconds, tcp_sent):
    latency_list = []
    #traffic dictionary by second
    traffic_list_temp = {0:0}
    tcp_goodput = 0
    second = 0
    tcp_drops = 0
    #print(q_seconds)
    for key in r_seconds:
        #try:
        thru_bytes = q_seconds[key][1]
        #self.traffic_raw.append(list((q_seconds[key][0],q_seconds[key][1])))
        # noting that the packet has been acked (once)
        q_seconds[key][2] -= 1
        tcp_goodput += thru_bytes
        second = int(math.floor(q_seconds[key][0]))
        if second in traffic_list_temp:
            traffic_list_temp[second] += thru_bytes
        else:
            traffic_list_temp[second] = thru_bytes
        r_time = r_seconds[key]
        q_time = q_seconds[key][0]
        latency_list.append(r_time - q_time)
    tcp_goodput_bytes = tcp_goodput
    tcp_goodput_Mbps = tcp_goodput_bytes / (125000.0 * second-1.0)
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
    fileNum = int(sys.argv[4])
    fileName = "trace_files/exp1_" + str(fileNum) + ".tr"
    outputFile = "exp2.txt"
    outputTrace = "pngs/exp1_" + str(fileNum) + ".txt"
    file1 = open(fileName, 'r')
    lines = file1.readlines()
    q1_sec, r1_sec, q2_sec, r2_sec, tcp1_sent, tcp2_sent = parse(lines)
    traffic1_list, tcp1_goodput_Mbps, tcp1_drop_rate, tcp1_latency = calculate(q1_sec, r1_sec, tcp1_sent)
    traffic2_list, tcp2_goodput_Mbps, tcp2_drop_rate, tcp2_latency = calculate(q2_sec, r2_sec, tcp2_sent)
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
    plt.plot(xs1, ys1_mbps, '-ok', label='1', color='b')
    plt.plot(xs2, ys2_mbps, '-ok', label='2', color='y')
    plt.legend()
    plt.grid(linestyle='-', linewidth='0.5', color='grey')
    plt.savefig("pngs/exp1_" + str(fileNum) + ".png")
    plt.clf()

    file1.close()

    print(fileName)

    write_string = ("tcpV: " + str(tcpV) + "; sec:" + str(sec) + "; mbps:" \
                 " " + str(mbps) + "; counter: " + str(fileNum) + "\n" \
                 "tcp1_drop_rate: " + str(tcp1_drop_rate) + "%; " \
                 "tcp1_goodput_Mbps: " + str(tcp1_goodput_Mbps) + "; " \
                 "tcp1_latency: " + str(tcp1_latency) + "\n")

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
                           "SimulationCounter": fileNum},
            "results": {"tcp1_drop_rate": tcp1_drop_rate,
                        "tcp1_goodput_Mbps": tcp1_goodput_Mbps,
                        "tcp1_latency": tcp1_latency,
                        "tcp2_drop_rate": tcp2_drop_rate,
                        "tcp2_goodput_Mbps": tcp2_goodput_Mbps,
                        "tcp2_latency": tcp2_latency}
           }
    json.dump(data, json_out, indent = 4)
    json_out.write('\n')
    json_out.close()  


if __name__ == "__main__":
    main()
