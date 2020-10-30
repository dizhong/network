
# use this to process the json file from parser and produce final graphs

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
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

    font = {'size':20}
    mpl.rc('font', **font)

    plt.xlim(0, 12)
    plt.xlabel("CBR flow size in Mbps")
    plt.ylabel("TCP average throughput in Mbps")
    plt.plot(x_t, y_t_t, '-ok', label='Tahoe', linestyle='--')
    plt.plot(x_r, y_r_t, '-ok', label='Reno', linestyle='-.')
    plt.plot(x_n, y_n_t, '-ok', label='NewReno', linestyle=':')
    plt.plot(x_v, y_v_t, '-ok', label='Vegas', linestyle='-')
    plt.legend(bbox_to_anchor= (0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0)
    plt.savefig("throughput.png", bbox_inches='tight')

    plt.clf()
    plt.xlim(0, 12)
    plt.xlabel("CBR flow size in Mbps")
    plt.ylabel("TCP drop rate in %")
    plt.plot(x_t, y_t_d, '-ok', label='Tahoe', linestyle='--')
    plt.plot(x_r, y_r_d, '-ok', label='Reno', linestyle='-.')
    plt.plot(x_n, y_n_d, '-ok', label='NewReno', linestyle=':')
    plt.plot(x_v, y_v_d, '-ok', label='Vegas', linestyle='-')
    plt.legend(bbox_to_anchor= (0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0)
    plt.savefig("droprate.png", bbox_inches='tight')

    plt.clf()
    plt.xlim(0, 12)
    plt.xlabel("CBR flow size in Mbps")
    plt.ylabel("TCP latency in Seconds")
    plt.plot(x_t, y_t_l, '-ok', label='Tahoe', linestyle='--')
    plt.plot(x_r, y_r_l, '-ok', label='Reno', linestyle='-.')
    plt.plot(x_n, y_n_l, '-ok', label='NewReno', linestyle=':')
    plt.plot(x_v, y_v_l, '-ok', label='Vegas', linestyle='-')
    plt.legend(bbox_to_anchor= (0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0)
    plt.savefig("latency.png", bbox_inches='tight')
    plt.clf()

    throughput_list = [y_t_t, y_r_t, y_n_t, y_v_t]
    droprate_list = [y_t_d, y_r_d, y_n_d, y_v_d]
    latency_list = [y_t_l, y_r_l, y_n_l, y_v_l]
    return throughput_list, droprate_list, latency_list

def main():
    fileName = "json.txt"
    tahoe, reno, newreno, vegas = get_data(fileName)
    throughput, droprate, latency = plot_graph(tahoe, reno, newreno, vegas)  
    #calculate t-test for select pairs
    ttest = open("ttest.txt", "w")
    against = ["Tahoe", "Reno", "NewReno"]
    #print(throughput)
    for i in range(0, 3):
        for m in range(0, 10):
            th_t, th_p = stats.ttest_ind(throughput[3][(m*4):((m+1)*4)], throughput[i][(m*4):((m+1)*4)])
            dr_t, dr_p = stats.ttest_ind(droprate[3][(m*4):((m+1)*4)], droprate[i][(m*4):((m+1)*4)])
            la_t, la_p = stats.ttest_ind(latency[3][(m*4):((m+1)*4)], latency[i][(m*4):((m+1)*4)])
            ttest.write("Vegas with " + against[i] + str(m) + "Mbps\n" \
                    "Throughput: t=" + str(th_t) + ", p=" + str(th_p) + "\n"\
                    "Droprate: t=" + str(dr_t) + ", p=" + str(dr_p) + "\n"\
                    "Latency: t=" + str(la_t) + ", p=" + str(la_p) + "\n")

    ttest.close()

if __name__ == "__main__":
    main()
