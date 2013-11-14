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
    print "successfully save a graph! hoho~"


'''
    Debug related functions
    Print Graph information
'''
def print_node_attr_names(graph):
    node_attr_v = snap.TStrV()
    graph.AttrNameNI(0, node_attr_v)
    for item in node_attr_v:
        print item  

def print_edge_attr_names(graph):
    edge_attr_v = snap.TStrV()
    graph.AttrNameEI(0, edge_attr_v)
    for item in edge_attr_v:
        print item

def print_nids(graph):
    nids = []
    for node in graph.Nodes():
        nids.append(node.GetId())
    nids.sort()
    print nids

'''
    Snapshot related functions
'''
# delete node based on its checkin starting timestamp
def filter_node_sts(graph, ts):
    for node in graph.Nodes():
        nid = node.GetId()
        print nid
        sts = graph.GetIntAttrDatN(nid, 'sts')
        #the node appears later than current timestamp
        if sts > ts:
            print sts, ts
            graph.DelNode(nid)


