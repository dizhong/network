import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from parser import Parser

def main():
    output = open("exp1.txt", "w")
    # for a range of texts
    for i in range(51, 397):
        # open them one by one
        file_name = "exp1_" + str(i) + ".tr"
        in_file = open(file_name, "r")
        lines = in_file.readlines()
        # pass to a new parser
        myParser = Parser(lines)
        myParser.run()
        # store useful parameters to appropriate data structure
        output.write("simulation" + str(i) + "\n" \
                     "tcp_drops " + str(myParser.tcp_drops) + "; " \
                     "tcp_goodput_bytes " + str(myParser.tcp_goodput_bytes) + "; " \
                     "tcp_goodput_Mbps " + str(myParser.tcp_goodput_Mbps) + "; " \
                     "tcp_latency " + str(myParser.tcp_latency) + "\n")
        xs = [x[0] for x in myParser.traffic_list]
        ys = [x[1] for x in myParser.traffic_list]
        ys_mbps = [(x/125000.0) for x in ys]
        plt.plot(xs, ys_mbps)
        png_name = "exp1_" + str(i) + ".png"
        plt.savefig(png_name)
        plt.close()
        # plot graphs
        in_file.close()
    # close output file
    output.close()

if __name__ == "__main__":
    main()
