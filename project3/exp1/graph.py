
# use this to process the json file from parser and produce final graphs

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import math
import sys
import json

#give a json file name and read in the data
def get_data(fileName):
#read in json file and produce needed data structures?
    jsonFile = open(fileName)
    thefile = jsonFile.read()
    decoder = json.JSONDecoder()
    #stores mbps, goodput, droprate, latency
    tahoe_data = []
    reno_data = []
    newreno_data = []
    vegas_data = []
    while (len(thefile) > 5):
        jsonData, s = decoder.raw_decode(thefile)
        thefile = thefile[s:].lstrip()
        results = jsonData["results"]
        parameters = jsonData["parameters"]
        if parameters["tcpVersion"] == 0:
            tahoe_data.append((parameters["CBRFlowMbps"],
                               results["tcp_goodput_Mbps"],
                               results["tcp_drop_rate"],
                               results["tcp_latency"]))
        elif parameters["tcpVersion"] == 1:
            reno_data.append((parameters["CBRFlowMbps"],
                               results["tcp_goodput_Mbps"],
                               results["tcp_drop_rate"],
                               results["tcp_latency"]))
        elif parameters["tcpVersion"] == 2:
            newreno_data.append((parameters["CBRFlowMbps"],
                               results["tcp_goodput_Mbps"],
                               results["tcp_drop_rate"],
                               results["tcp_latency"]))
        elif parameters["tcpVersion"] == 3:
            vegas_data.append((parameters["CBRFlowMbps"],
                               results["tcp_goodput_Mbps"],
                               results["tcp_drop_rate"],
                               results["tcp_latency"]))
        else:
            print("error in tcp version #")
        
    return tahoe_data, reno_data, newreno_data, vegas_data
        


#need 3 graphs: average throughput, average drop, average latency
#can probably plot 4 lines in eachi
def plot_graph(tahoe, reno, newreno, vegas):
    x_t = [x[0] for x in tahoe]
    y_t_t = [x[1] for x in tahoe]
    y_t_d = [x[2] for x in tahoe]
    y_t_l = [x[3] for x in tahoe]
    x_r = [x[0] for x in reno]
    y_r_t = [x[1] for x in reno]
    y_r_d = [x[2] for x in reno]
    y_r_l = [x[3] for x in reno]
    x_n = [x[0] for x in newreno]
    y_n_t = [x[1] for x in newreno]
    y_n_d = [x[2] for x in newreno]
    y_n_l = [x[3] for x in newreno]
    x_v = [x[0] for x in vegas]
    y_v_t = [x[1] for x in vegas]
    y_v_d = [x[2] for x in vegas]
    y_v_l = [x[3] for x in vegas]

    plt.xlim(0, 12)
    plt.plot(x_t, y_t_t, '-ok', label='Tahoe', color='k')
    plt.plot(x_r, y_r_t, '-ok', label='Reno', color='y')
    plt.plot(x_n, y_n_t, '-ok', label='NewReno', color='g')
    plt.plot(x_v, y_v_t, '-ok', label='Vegas', color='b')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig("throughput.png")

    plt.clf()
    plt.xlim(0, 12)
    plt.plot(x_t, y_t_d, '-ok', label='Tahoe', color='k')
    plt.plot(x_r, y_r_d, '-ok', label='Reno', color='y')
    plt.plot(x_n, y_n_d, '-ok', label='NewReno', color='g')
    plt.plot(x_v, y_v_d, '-ok', label='Vegas', color='b')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig("droprate.png")

    plt.clf()
    plt.xlim(0, 12)
    plt.plot(x_t, y_t_l, '-ok', label='Tahoe', color='k')
    plt.plot(x_r, y_r_l, '-ok', label='Reno', color='y')
    plt.plot(x_n, y_n_l, '-ok', label='NewReno', color='g')
    plt.plot(x_v, y_v_l, '-ok', label='Vegas', color='b')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig("latency.png")
    plt.clf()



def main():
    fileName = "json.txt"
    tahoe, reno, newreno, vegas = get_data(fileName)
    plot_graph(tahoe, reno, newreno, vegas)  


if __name__ == "__main__":
    main()
