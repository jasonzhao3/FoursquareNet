import snap
import random
import os
	
def gen_degree_hist( graph ):
	deg_cnt_v = snap.TIntPrV()
	snap.GetDegCnt( graph, deg_cnt_v )
	return deg_cnt_v


# load graph 
def LoadGraph(data_path, filename):
	graph_in = snap.TFIn(os.path.join(data_path, filename))
	graph_out = snap.TNEANet.Load(graph_in)
	return graph_out


