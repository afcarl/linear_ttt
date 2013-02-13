import csv
import os
import matplotlib.pyplot as plt
import sys

features = [15, 30, 45, 60, 75, 100]
thresholds = [0, 1, 2, 3]
headers = ['Episodes','P1-Win','P1-Lose','P1-Draw','P2-Win','P2-Lose','P2-Draw']
colors = ['red','blue','yellow', 'green', 'orange', 'purple', 'brown'] # max 7 lines
fileformat = "kanerva_{0}_features_and_{1}_threshold_average.csv"

data = []
for t in thresholds:
    series = [[] for h in range(1,len(headers))]
    data.append(series)
    for feature in features:
        filename = fileformat.format(feature, t)
        f = open(filename, 'r')
        reader = csv.reader(f)
        last = reader.next()
        for row in reader:
            last = row
        for i,v in enumerate(last):
            if i > 0:
                series[i-1].append(float(row[i]))

for graph in range(0,len(headers)-1):
    ax = plt.subplot(111)
    for threshold,series in enumerate(data):
        print 'graph: {0} threshold: {1} len(series): {2}'.format(graph,threshold,len(series))
        plt.plot(features, series[graph], label='{0} threshold'.format(threshold), color=colors[threshold])
    plt.xlabel("# Features")
    plt.ylabel('Probability')
    plt.ylim([0,1])
    plt.title('Kanerva Analysis\n({0})'.format(headers[graph+1]))
    # Shink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('kanerva_{0}.png'.format(headers[graph+1].replace(' ','_').lower()))
    plt.clf()
