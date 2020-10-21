#!/usr/bin/env python3

# This file is used to analyze the ns2 trace files by batch

#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import numpy as np
#from pylab import cm

# The Parser class processes the individual trace files
class Parser:
    def __init__(self, trace_list):
        self.trace = trace_list
        self.tcp_goodput_byte = 0.0
        self.tcp_goodput_Mbps = 0.0
        self.tcp_latency = None
        self.tcp_drops = None
 

    # first put all values into their lists?
    def parse(self):
        if self.trace == None or len(self.trace) < 1:
            print("trace file empty \n")
            return
        # only keep timestamp and packet# and received packet size
        queued = 0
        received = 0
        q_seconds = {}
        r_seconds = {}
        for line in self.trace:
            split = line.split(" ")
            if split[4] == "tcp" and split[0] == "+" and split[2] == "0":
                q_seconds[int(split[10])] = (float(split[1]), int(split[5]))
            elif split[4] == "ack" and split[0] == "r" and split[3] == "0":
                key = int(split[10])
                if key not in r_seconds:
                    r_seconds[key] = float(split[1])
        #print(q_seconds)
        #print(r_seconds)
        self.calculate(q_seconds, r_seconds)


    # then calculate the averages and sums
    def calculate(self, q_seconds, r_seconds):
        latency_list = []
        tcp_goodput = 0
        #print(r_seconds)
        for key in r_seconds:
            try:
                tcp_goodput += q_seconds[key][1]
            except KeyError:
                print(q_seconds)
            r_time = r_seconds[key]
            #print(triple[0])
            q_time = q_seconds[key][0]
            latency_list.append(r_time - q_time)
        # number of drops is number of items left in dictionary
        self.tcp_drops = len(q_seconds)
        # time is consistently 5 seconds
        self.tcp_goodput_bytes = tcp_goodput
        self.tcp_goodput_Mbps = self.tcp_goodput_bytes / (125000.0 * 61.0)
        self.tcp_latency = sum(latency_list) / len(latency_list)
        print(len(r_seconds))
        print("above size of acks")
        print(len(q_seconds))
        print("above size of packets")
        

# main feeds files into parser, and produce graphs
def main():
    file1 = open('exp1.tr', 'r')
    lines = file1.readlines()
    myparser = Parser(lines)
    myparser.parse()
    print(myparser.tcp_drops)
    print(myparser.tcp_goodput_bytes)
    print(myparser.tcp_goodput_Mbps)
    print(myparser.tcp_latency)



if __name__ == "__main__":
    main()
