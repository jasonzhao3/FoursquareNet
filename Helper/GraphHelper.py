import snap
import random
import os
	
def gen_degree_hist( graph ):
	deg_cnt_v = snap.TIntPrV()
	snap.GetDegCnt( graph, deg_cnt_v )
	return deg_cnt_v


# load graph 
def load_graph(data_path, filename):
	graph_in = snap.TFIn(os.path.join(data_path, filename))
	graph_out = snap.TNEANet.Load(graph_in)
	return graph_out

def save_graph(graph, data_path, filename):
    out_file = os.path.join(data_path, filename)
    graph_out = snap.TFOut(out_file)
    graph.Save(graph_out)
    graph_out.Flush()

