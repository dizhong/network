
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
    R_DT_data = []
    R_RED_data = []
    S_DT_data = []
    S_RED_data = []
    while (len(thefile) > 5):
        sublist = []
        #for i in range(1, 9):
        jsonData, s = decoder.raw_decode(thefile)
        thefile = thefile[s:].lstrip()
        results = jsonData["results"]
        parameters = jsonData["parameters"]
        sublist = list((parameters["CBRStartSec"],
                       results["tcp_goodput_Mbps"],
                       results["cbr_goodput_Mbps"],
                       results["tcp_drop_rate"],
                       results["cbr_drop_rate"],
                       results["tcp_latency"],
                       results["cbr_latency"]))
        #data = np.array(sublist)
        #sublist = data.mean(axis=0)
        if (parameters["tcpVersion"] == 0) and (parameters["Queuing"] == "DropTail"):
            R_DT_data.append(sublist)
        elif (parameters["tcpVersion"] == 0) and (parameters["Queuing"] == "RED"):
            R_RED_data.append(sublist)
        elif (parameters["tcpVersion"] == 1) and (parameters["Queuing"] == "DropTail"):
            S_DT_data.append(sublist)
        elif (parameters["tcpVersion"] == 1) and (parameters["Queuing"] == "RED"):
            S_RED_data.append(sublist)
        else:
            print("error in tcp version #")
    #print(R_DT_data)
    return R_DT_data, R_RED_data, S_DT_data, S_RED_data
        


#need 3 graphs: average throughput, average drop, average latency
#can probably plot 4 lines in eachi
def plot_graph(rdt, rred, sdt, sred):
    pair_names = [("Reno Droptail", "CBR"), ("Reno RED", "CBR"), ("SACK DropTail", "CBR"), ("SACK RED", "CBR")]
    png_kinds = ["throughput", "droprate", "latency"]
    x_axis = []
    throughput_y = []
    droprate_y = []
    latency_y = []
    raw_data = [rdt, rred, sdt, sred]
    x_axis = [x[0] for x in rdt]
    #counter=0
    for data_list in raw_data:
        #print(data_list)
        #counter += 1
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

    font = {'size': 20}
    mpl.rc('font', **font)
    #plt.figure(figsize=(20, 10))
    flow_names = ['TCP', 'CBR']
    png_kinds = ['Throughput', 'Droprate', 'Latency']
    png_desc = [" Average Throughput in Mbps", " Average Droprate in %", " Average Latency in Seconds"]
    for png_kind in range(0, 3):
        for flow_kind in range(0, 2):
            plt.xlim(15, 60)
            plt.xlabel(flow_names[flow_kind] + " flow start time in Seconds")
            plt.ylabel(flow_names[flow_kind] + png_desc[png_kind])
            plt.plot(x_axis, y_axis[png_kind][0][flow_kind], '-ok', linestyle='-', label="Reno+DT")
            plt.plot(x_axis, y_axis[png_kind][1][flow_kind], '-ok', linestyle='-.', label="Reno+RED")
            plt.plot(x_axis, y_axis[png_kind][2][flow_kind], '-ok', linestyle='--', label="SACK+DT")
            plt.plot(x_axis, y_axis[png_kind][3][flow_kind], '-ok', linestyle=':', label="SACK+RED")
            plt.legend(bbox_to_anchor= (0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0)
            plt.savefig(flow_names[flow_kind] + png_kinds[png_kind] + ".png", bbox_inches='tight')
            plt.clf()

    return y_axis, pair_names, png_kinds



def main():
    fileName = "json.txt"
    R_DT_data, R_RED_data, S_DT_data, S_RED_data = get_data(fileName)
    y_axis, pair_names, data_kinds = plot_graph(R_DT_data, R_RED_data, S_DT_data, S_RED_data)  
    
    #calculate t-test and general avverage
    ttest = open("ttest.txt", "w")
    averages = open("averages.txt", "w")
    for data_kind in range(0, 3):
        current_y = y_axis[data_kind]
        for pair_num in range(0, 4):
            current_pair = current_y[pair_num]
            t_value, p_value = stats.ttest_ind(current_pair[0], current_pair[1])
            ttest.write(pair_names[pair_num][0] + pair_names[pair_num][1] + ":"\
                        " " + data_kinds[data_kind] + "\nt_value:" \
                        " " + str(t_value) + " p_value: " + str(p_value) + "\n")
            average_0 = sum(current_pair[0]) / len(current_pair[0])
            average_1 = sum(current_pair[1]) / len(current_pair[1])
            averages.write(pair_names[pair_num][0] + " Average " + data_kinds[data_kind] + ": " + str(average_0) + "\n")
            averages.write(pair_names[pair_num][1] + " Average " + data_kinds[data_kind] + ": " + str(average_1) + "\n")

    #calculate one-way anova
    th_array = y_axis[0]
    dr_array = y_axis[1]
    la_array = y_axis[2]
    th_anova_f, th_anova_p = stats.f_oneway(th_array[0], th_array[1], th_array[2], th_array[3])
    print("Anova throughput: \nF: " + str(th_anova_f) + "P: " + str(th_anova_p))
    dr_anova_f, dr_anova_p = stats.f_oneway(dr_array[0], dr_array[1], dr_array[2], dr_array[3])
    print("Anova droprate: \nF: " + str(dr_anova_f) + "P: " + str(dr_anova_p))
    la_anova_f, la_anova_p = stats.f_oneway(la_array[0], la_array[1], la_array[2], la_array[3])
    print("Anova latency: \nF: " + str(la_anova_f) + "P: " + str(la_anova_p))

    #calculate t-tests
    


    ttest.close()
    averages.close()
    


if __name__ == "__main__":
    main()
