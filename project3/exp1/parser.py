#!/usr/bin/env python3

# This file is used to analyze the ns2 trace files by batch

import matplotlib as mpl
import matplotlib.pyplot as plt
import math
#import numpy as np
#from pylab import cm

# The Parser class processes the individual trace files
class Parser:
    def __init__(self, trace_list):
        self.trace = trace_list
        self.tcp_goodput_bytes = 0.0
        self.tcp_goodput_Mbps = 0.0
        self.tcp_latency = None
        self.tcp_drops = None
        self.traffic_list = []
 

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
            #store parameters of the traces of packets that were queued to send
            if split[4] == "tcp" and split[0] == "+" and split[2] == "0":
                q_seconds[key] = (float(split[1]), int(split[5]))
            #store parameters of the traces of acks that were received
            elif split[4] == "ack" and split[0] == "r" and split[3] == "0":
                if key not in r_seconds:
                    r_seconds[key] = float(split[1])
            elif split[0] == "d" and (split[4] == "ack" or split[4] == "tcp"):
                dropped.append(line)
        #print(len(dropped))
        #print("above dropped")
        #print(q_seconds)
        print(r_seconds)
        print(counter)
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
            tcp_goodput += thru_bytes
            second = int(math.floor(q_seconds[key][0]))
            #print(second)
            if second in traffic_list_temp:
                traffic_list_temp[second] += thru_bytes
            else:
                traffic_list_temp[second] = thru_bytes
            r_time = r_seconds[key]
            q_time = q_seconds[key][0]
            latency_list.append(r_time - q_time)
        self.tcp_drops = len(dropped)
        self.tcp_goodput_bytes = tcp_goodput
        self.tcp_goodput_Mbps = self.tcp_goodput_bytes / (125000.0 * second-1.0)
        self.tcp_latency = sum(latency_list) / len(latency_list)
        
        self.traffic_list = [(k, v) for k, v in sorted(traffic_list_temp.items())]
        #self.traffic_list = self.traffic_list[:60]
        #print(len(r_seconds))
        #print("above size of acks")
        #print(len(q_seconds))
        #print("above size of packets")

    # function to run the other two
    def run(self):
        q_seconds, r_seconds, dropped = self.parse()
        self.calculate(q_seconds, r_seconds, dropped)
                

# main feeds files into parser, and produce graphs
def main():
    file1 = open('exp1_173.tr', 'r')
    lines = file1.readlines()
    myparser = Parser(lines)
    myparser.run()
    xs = [x[0] for x in myparser.traffic_list]
    ys = [x[1] for x in myparser.traffic_list]
    ys_mbps = [ (x / 125000.0) for x in ys]
    plt.plot(xs, ys_mbps)
    plt.savefig("exp1_173.png")
    print(myparser.traffic_list)
    print(ys_mbps)
    print(myparser.tcp_drops)
    print(myparser.tcp_goodput_bytes)
    print(myparser.tcp_goodput_Mbps)
    print(myparser.tcp_latency)



if __name__ == "__main__":
    main()
