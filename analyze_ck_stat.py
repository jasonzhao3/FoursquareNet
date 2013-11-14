'''
    This script is used to analyze the the distribution of check-ins
'''
import snap
import os, pickle
import numpy as np
import Helper.GraphHelper as GH
import collections as cl
import pylab as plt

''' Import Graph: graph is stored in binary form to save space, available in dropbox folder
    sf_trsn_graph_small: A small test graph with only a few venues in sf -- you can use this to test your script first
    sf_trsn_graph: up-to-date venue graph of sf
'''

def counter_to_arrays(c):
	values = []
	frequencies = []
	for n in c:
		values.append(n)
		frequencies.append(c[n])
	return [values, frequencies]

data_path = '../CS224W_Dataset/GraphData'
result_path = '../CS224W_Dataset/Analysis/'

graph = GH.load_graph(data_path, 'sf_venue_graph')
occurrences = cl.Counter()

for node in graph.Nodes():
	ckn = graph.GetIntAttrDatN(node.GetId(), 'ckn')
	occurrences[ckn] += 1

x, y = counter_to_arrays(occurrences)

plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.scatter(x, y, color='crimson')
plt.title('check-in distribution of venues')
plt.ylabel('number of venues')
plt.xlabel('total check-ins')
plt.savefig(os.path.join(result_path, 'ck_freq_dist.png'))

occurrences = cl.Counter()
for edge in graph.Edges():
	trsn_cnt = graph.GetIntAttrDatE(edge.GetId(), 'trsn_cnt')
	occurrences[trsn_cnt] += 1

x, y = counter_to_arrays(occurrences)

plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.scatter(x, y, color='crimson')
plt.title('transition counts distribution')
plt.ylabel('number of edges')
plt.xlabel('transition counts')
plt.savefig(os.path.join(result_path, 'trsn_counts_dist.png'))

