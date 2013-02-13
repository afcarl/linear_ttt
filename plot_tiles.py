import csv
import os
import matplotlib.pyplot as plt
import sys

features = [5, 10, 16, 20, 25, 30, 50]
headers = ['Episodes','P1-Win','P1-Lose','P1-Draw','P2-Win','P2-Lose','P2-Draw']
colors = ['red','blue','yellow', 'green', 'orange', 'purple', 'brown'] # max 7 lines
fileformat = "random_{0}_tiles_average.csv"

series = [[] for h in range(1,len(headers))]
for feature in features:
    filename = fileformat.format(feature)
    f = open(filename, 'r')
    reader = csv.reader(f)
    last = reader.next()
    for row in reader:
        last = row
    for i,v in enumerate(last):
        if i > 0:
            series[i-1].append(float(row[i]))

for graph in range(0,len(headers)-1):
    print 'graph: {0} feature: {1}'.format(graph,features[graph])
    plt.plot(features, series[graph], label=headers[graph+1], color=colors[graph])
plt.xlabel("# Tiles")
plt.ylabel('Probability')
plt.ylim([0,1])
plt.title('Kanerva Analysis\n({0})'.format("random tiles"))

ax = plt.subplot(111)
# Shink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig('random_tiles.png')
    #plt.clf()
