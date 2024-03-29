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
class Parser:
    def __init__(self, trace_list):
        self.trace = trace_list
        self.tcp_goodput_bytes = 0.0
        self.tcp_goodput_Mbps = 0.0
        self.tcp_latency = None
        self.tcp_drops = 0
        self.tcp_sent = 0
        self.traffic_list = []
        self.traffic_raw = []
 

    # first put all values into their lists?
    def parse(self):
        if self.trace == None or len(self.trace) < 1:
            print("trace file empty \n")
            return
        # only keep timestamp and packet# and received packet size
        q_seconds = {}
        r_seconds = {}
        dropped = []
        counter = 0
        print(self.trace[-1])
        for line in self.trace:
            counter += 1
            split = line.split(" ")
            key = int(split[10])
            if float(split[1]) >= 5:
                #store parameters of the traces of packets that were queued to send
                if split[4] == "tcp" and split[0] == "+" and split[2] == "0":
                    if key in q_seconds:
                        q_seconds[key][2] += 1
                        self.tcp_sent += 1
                    else:
                        q_seconds[key] = list((float(split[1]), int(split[5]), 1))
                        self.tcp_sent += 1
                #store parameters of the traces of acks that were received
                elif split[4] == "ack" and split[0] == "r" and split[3] == "0" and key in q_seconds:
                    if key not in r_seconds:
                        r_seconds[key] = float(split[1])
        return q_seconds, r_seconds, dropped


    # then calculate the averages and sums
    def calculate(self, q_seconds, r_seconds, dropped):
        latency_list = []
        #traffic dictionary by second
        traffic_list_temp = {0:0}
        tcp_goodput = 0
        second = 0
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
        self.tcp_goodput_bytes = tcp_goodput
        self.tcp_goodput_Mbps = self.tcp_goodput_bytes / (125000.0 * 120)
        self.tcp_latency = sum(latency_list) / len(latency_list)
        
        # find the number of dropped packets by counting all the packets
        # that were sent and not acked (including the retransmitted ones
        for key in q_seconds:
            self.tcp_drops += q_seconds[key][2]
        # normalize the list to include 0 when there is no throughput
        for i in range(0, 125):
            if i not in traffic_list_temp:
                traffic_list_temp[i] = 0
        self.traffic_list = [(k,v) for k,v in sorted(traffic_list_temp.items())]

    # function to run the other two
    def run(self):
        q_seconds, r_seconds, dropped = self.parse()
        self.calculate(q_seconds, r_seconds, dropped)
                

# main feeds files into parser, and produce graphs
def main():
    tcpV = int(sys.argv[1])
    tcpSec = int(sys.argv[2])
    mbps = int(sys.argv[3])
    fileNum = int(sys.argv[4])
    fileName = "trace_files/exp1_" + str(fileNum) + ".tr"
    outputFile = sys.argv[5]
    outputTrace = "pngs/exp1_" + str(fileNum) + ".txt"
    file1 = open(fileName, 'r')
    lines = file1.readlines()
    myparser = Parser(lines)
    myparser.run()
    xs = [x[0] for x in myparser.traffic_list]
    ys = [x[1] for x in myparser.traffic_list]
    ys_mbps = [ (x / 125000.0) for x in ys]
    plt.ylim(0, 11)
    plt.xlim(0, 130)
    plt.xlabel("Seconds")
    plt.ylabel("Mbps")
    plt.plot(xs, ys_mbps, '-ok')
    plt.grid(linestyle='-', linewidth='0.5', color='grey')
    plt.savefig("pngs/exp1_" + str(fileNum) + ".png")
    plt.clf()

    file1.close()

    print(fileName)

    pkt_drop_rate = (myparser.tcp_drops / float(myparser.tcp_sent)) * 100

    write_string = ("tcpV: " + str(tcpV) + "; tcpSec: " + str(tcpSec) + ";"\
                  " mbps:" \
                 " " + str(mbps) + "; counter: " + str(fileNum) + "\n" \
                 "tcp_drops: " + str(myparser.tcp_drops) + "; " \
                 "tcp_drop_rate: " + str(pkt_drop_rate) + "%; " \
                 "tcp_goodput_bytes: " + str(myparser.tcp_goodput_bytes) + "; " \
                 "tcp_goodput_Mbps: " + str(myparser.tcp_goodput_Mbps) + "; " \
                 "tcp_latency: " + str(myparser.tcp_latency) + "\n")

    print(write_string)

    output = open(outputFile, "a")
    output.write(write_string)
    output.close()

    output2 = open(outputTrace, "w")
    output2.write(write_string)
    output2.write(str(xs) + "\n")
    output2.write(str(ys_mbps))
    output2.close()

    json_out = open('json.txt', "a")
    data = {}
    data = {"parameters": {"tcpVersion": tcpV,
                           "TCPStartSec": tcpSec, 
                           #"CBRStartSec": cbrSec,
                           "CBRFlowMbps":  mbps, 
                           "SimulationCounter": fileNum},
            "results": {"tcp_drops": myparser.tcp_drops,
                        "tcp_drop_rate": pkt_drop_rate,
                        "tcp_goodput_bytes": myparser.tcp_goodput_bytes,
                        "tcp_goodput_Mbps": myparser.tcp_goodput_Mbps,
                        "tcp_latency": myparser.tcp_latency}
           }
    json.dump(data, json_out, indent = 4)
    json_out.write('\n')
    json_out.close()  


if __name__ == "__main__":
    main()
