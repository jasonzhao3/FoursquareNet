''' In this cript, we will do a series of analysis,
    Just follow this template, build your own analysis script,
    and try to play with the graph :) '''

import snap
import os
import numpy as np
import Helper.GraphHelper as GH
import pylab as plt

''' Import Graph: graph is stored in binary form to save space, available in dropbox folder
    sf_trsn_graph_small: A small test graph with only a few venues in sf -- you can use this to test your script first
    sf_trsn_graph: up-to-date venue graph of sf
'''
data_path = '../DataSet/'
result_path = '../DataSet/Analysis/'
graph_in = snap.TFIn(os.path.join(data_path, 'sf_trsn_graph'))
trsn_g = snap.TNEANet.Load(graph_in)


'''Analysis 1: graph structure
   - graph size
   - SCC, bowtie structure
'''
g_size = trsn_g.GetNodes()
edge_size = trsn_g.GetEdges()
max_scc = snap.GetMxScc(trsn_g)
num_max_scc_n = max_scc.GetNodes()
rand_node = max_scc.GetRndNId()
out_combined = snap.GetBfsTree( trsn_g, rand_node, True, False )
in_combined = snap.GetBfsTree( trsn_g, rand_node, False, True )

max_wcc = snap.GetMxWcc( trsn_g )
num_max_wcc_n = max_wcc.GetNodes()

num_out = out_combined.GetNodes() - num_max_scc_n
num_in = in_combined.GetNodes() - num_max_scc_n
numDiscon = g_size - num_max_wcc_n
print "The size of the graph is %d, %d" %(g_size, edge_size)
print "The largest SCC ratio is: %0.4f " %( float(num_max_scc_n) / g_size )
print "The In-component of the largest SCC ratio is: %0.4f "  %(float(num_in) / g_size)
print "The Out-component of the largest SCC ratio is: %0.4f"  % (float(num_out) / g_size)
print "The disconnected components has the percentage: %0.4f"  % (float(numDiscon) / g_size)


''' Analysis 2: graph structure
    - node distribution
'''
deg_cnt_v = GH.gen_degree_hist(trsn_g)
deg_v, deg_prob = zip(*[[item.GetVal1(), float(item.GetVal2()) / g_size] for item in deg_cnt_v])

plt.figure()
plt.plot(deg_v, deg_prob, '-yo', color='red', label='node degreee distribution')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.title('log-log node degree distribution of transition graph')
plt.savefig(os.path.join(result_path, 'node_dist.png'))


'''Analysis 3: edge(trasition) freatures
   - transition frequency distribution
   - transition duration distribution
'''
trsn_freqs = []
trsn_durations = []
for edge in trsn_g.Edges():
    src_nid = edge.GetSrcNId()
    dst_nid = edge.GetDstNId()
    edge_id = trsn_g.GetEId(src_nid, dst_nid)
    freq = trsn_g.GetIntAttrDatE(edge_id, 'freq')
    if freq > 20:
        trsn_freqs.append(freq)
    trsn_durations.append(trsn_g.GetFltAttrDatE(edge_id, 'duration'))
print max(trsn_freqs), len(trsn_freqs)
trsn_freqs = np.log(np.array(trsn_freqs)+10)
trsn_durations = np.array(trsn_durations) / 60.0

plt.figure()
plt.hist(trsn_freqs, bins=50, label='transition frequency')
plt.title('transition frequency distribution > 20')
plt.ylabel('number)')
plt.xlabel('transition frequency -- log(#+10)')
plt.savefig(os.path.join(result_path, 'trsn_freq_dist.png'))

plt.figure()
plt.hist(trsn_durations, bins=30, label='transition duration')
plt.xlabel('duration/10min')
plt.ylabel('number')
plt.title('transition duration distribution')
plt.savefig(os.path.join(result_path, 'trsn_duration_dist.png'))
    
