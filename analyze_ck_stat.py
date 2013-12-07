'''
    This script is used to analyze the the distribution of check-ins
'''
import snap
import os, pickle
import numpy as np
import Helper.GraphHelper as GH
import Helper.AnalysisHelper as AH
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

data_path = '../Dataset/GraphData'
result_path = '../Dataset/Analysis/'

graph = GH.load_graph(data_path, 'sf_venue_graph')
occurrences = cl.Counter()
dataset = []

for node in graph.Nodes():
	ckn = graph.GetIntAttrDatN(node.GetId(), 'ckn')
	occurrences[ckn] += 1
	dataset.append(ckn)

x, y = counter_to_arrays(occurrences)
alpha = AH.get_mle_alpha(dataset, min(dataset))
powerlaw_y = AH.get_powerlaw_y(dataset, alpha, min(dataset), np.sum(y))   
print "check-in distribution: the estimated alpha is", alpha

plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.scatter(x, y, color='crimson', label='check-in distribution')
plt.plot(powerlaw_y, color='blue', label='MLE-PDF alpha: ' + str(alpha)[:4])
plt.title('check-in distribution of venues')
plt.ylabel('number of venues')
plt.xlabel('total check-ins')
plt.legend()
plt.savefig(os.path.join(result_path, 'ck_freq_dist.png'))

occurrences = cl.Counter()
dataset = []
for edge in graph.Edges():
	trsn_cnt = graph.GetIntAttrDatE(edge.GetId(), 'trsn_cnt')
	occurrences[trsn_cnt] += 1
	dataset.append(trsn_cnt)

x, y = counter_to_arrays(occurrences)
alpha = AH.get_mle_alpha(dataset, min(dataset))
powerlaw_y = AH.get_powerlaw_y(dataset, alpha, min(dataset), np.sum(y))   
print "transition counts distribution: the estimated alpha is", alpha

plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.scatter(x, y, color='crimson', label='transition counts distribution')
#plt.plot(powerlaw_y[3:200], color='blue', label='MLE-PDF alpha: ' + str(alpha)[:4])
plt.title('transition counts distribution')
plt.ylabel('number of edges')
plt.xlabel('transition counts')
plt.legend()
plt.savefig(os.path.join(result_path, 'trsn_counts_dist.png'))

