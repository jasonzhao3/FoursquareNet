import snap
import os
import numpy as np

data_path = '../DataSet/'
graph_in = snap.TFIn(os.path.join(data_path, 'sf_trsn_graph_small'))

trsn_g = snap.TNEANet.Load(graph_in)
g_size = trsn_g.GetNodes()
print "The size of the graph is %d" %(g_size)

max_scc = snap.GetMxScc(trsn_g)
num_max_scc_n = max_scc.GetNodes()
print "The largest SCC ratio is: %0.4f " %( float(num_max_scc_n) / g_size )

randNode = max_scc.GetRndNId()
outCombined = snap.GetBfsTree( trsn_g, randNode, True, False )
inCombined = snap.GetBfsTree( trsn_g, randNode, False, True )

max_wcc = snap.GetMxWcc( trsn_g )
num_max_wcc_n = max_wcc.GetNodes()

num_out = outCombined.GetNodes() - num_max_scc_n
num_in = inCombined.GetNodes() - num_max_scc_n
numDiscon = g_size - num_max_wcc_n
print "The In-component of the largest SCC ratio is: %0.4f "  %(float(num_in) / g_size)
print "The Out-component of the largest SCC ratio is: %0.4f"  % (float(num_out) / g_size)
print "The disconnected components has the percentage: %0.4f"  % (float(numDiscon) / g_size)

