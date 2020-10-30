
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
    RR_data = []
    NR_data = []
    VV_data = []
    NV_data = []
    while (len(thefile) > 5):
        sublist = []
        for i in range(1, 11):
            jsonData, s = decoder.raw_decode(thefile)
            thefile = thefile[s:].lstrip()
            results = jsonData["results"]
            parameters = jsonData["parameters"]
            sublist.append(list((parameters["CBRFlowMbps"],
                       results["tcp1_goodput_Mbps"],
                       results["tcp2_goodput_Mbps"],
                       results["tcp1_drop_rate"],
                       results["tcp2_drop_rate"],
                       results["tcp1_latency"],
                       results["tcp2_latency"])))
        data = np.array(sublist)
        mean = data.mean(axis=0)
        err = data.std(axis=0)
        sublist = tuple(zip(mean, err))
        if parameters["tcpVersion"] == 0:
            RR_data.append(sublist)
        elif parameters["tcpVersion"] == 1:
            NR_data.append(sublist)
        elif parameters["tcpVersion"] == 2:
            VV_data.append(sublist)
        elif parameters["tcpVersion"] == 3:
            NV_data.append(sublist)
        else:
            print("error in tcp version #")
        
    return RR_data, NR_data, VV_data, NV_data
        


#need 3 graphs: average throughput, average drop, average latency
#can probably plot 4 lines in eachi
def plot_graph(rr, nr, vv, nv):
    pair_names = [("Reno", "Reno"), ("NewReno", "Reno"), ("Vegas", "Vegas"), ("NewReno", "Vegas")]
    png_kinds = ["throughput", "droprate", "latency"]
    x_axis = []
    throughput_y = []
    droprate_y = []
    latency_y = []
    raw_data = [rr, nr, vv, nv]
    x_axis = [x[0][0] for x in rr]
    for data_list in raw_data:
        throughput_y_1 = [x[1] for x in data_list]
        throughput_y_2 = [x[2] for x in data_list]
        throughput_y.append(list(((throughput_y_1), (throughput_y_2))))
        droprate_y_1 = [x[3] for x in data_list]
        droprate_y_2 = [x[4] for x in data_list]
        droprate_y.append(list(((droprate_y_1), (droprate_y_2))))
        latency_y_1 = [x[5] for x in data_list]
        latency_y_2 = [x[6] for x in data_list]
        latency_y.append(list(((latency_y_1), (latency_y_2))))

    y_axis = [throughput_y, droprate_y, latency_y]

    #print(y_axis)
    #print(x_axis)
    reconstruct_y = []
    for png_kind in range(0, 3):
        current_y = y_axis[png_kind]
        reconstruct_y_sub = []
        for pair_num in range(0, 4):
            current_pair_0 = current_y[pair_num][0]
            current_pair_1 = current_y[pair_num][1]
            mean_0 = np.array([x[0] for x in current_pair_0])
            err_0 = np.array([x[1] for x in current_pair_0])
            mean_1 = np.array([x[0] for x in current_pair_1])
            err_1 = np.array([x[1] for x in current_pair_1])
            x_axis = np.array(x_axis)
            #print(current_pair_0)
            #if (png_kind == 2) and (pair_num == 0):
            #    print(current_pair)
            print(x_axis)
            print(mean_0)
            print(err_0)
            plt.xlim(0, 12)
            plt.errorbar(x_axis, mean_0, yerr=err_0, label=pair_names[pair_num][0], color='k')
            plt.errorbar(x_axis, mean_1, yerr=err_1, label=pair_names[pair_num][1], color='y')
            plt.legend(bbox_to_anchor= (0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0)
            plt.savefig(png_kinds[png_kind] + pair_names[pair_num][0] + pair_names[pair_num][1] + ".png")
            plt.clf()

    return y_axis, pair_names, png_kinds


def main():
    fileName = "json.txt"
    tahoe, reno, newreno, vegas = get_data(fileName)
    y_axis, pair_names, data_kinds = plot_graph(tahoe, reno, newreno, vegas)  
    #calculate t-test
    ttest = open("ttest.txt", "w")
    for data_kind in range(0, 3):
        current_y = y_axis[data_kind]
        for pair_num in range(0, 4):
            current_pair = current_y[pair_num]
            t_value, p_value = stats.ttest_ind(current_pair[0], current_pair[1])
            ttest.write(pair_names[pair_num][0] + pair_names[pair_num][1] + ":"\
                        " " + data_kinds[data_kind] + "\nt_value:" \
                        " " + str(t_value) + " p_value: " + str(p_value) + "\n")

    ttest.close()




if __name__ == "__main__":
    main()
