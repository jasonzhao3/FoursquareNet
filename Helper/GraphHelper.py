import snap
import random
import os
	
def gen_degree_hist( graph ):
	deg_cnt_v = snap.TIntPrV()
	snap.GetDegCnt( graph, deg_cnt_v )
	return deg_cnt_v


'''
    Save and Load Graph
'''
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
    Node and Edge attribute related functions
    ------------------------------------------
'''
def add_time_stamp(graph, nid, time_stamp):
    #the type bug was weird, has trapped me for a while
    graph.AddIntAttrDatN(nid, int(time_stamp), 'sts')
    graph.AddIntAttrDatN(nid, int(time_stamp), 'ets')


def update_time_stamp(graph, nid, time_stamp):
    time_stamp = int(time_stamp)
    old_sts = graph.GetIntAttrDatN(nid, 'sts')
    old_ets = graph.GetIntAttrDatN(nid, 'ets')
    if time_stamp < old_sts:
        graph.AddIntAttrDatN(nid, time_stamp, 'sts')
    elif time_stamp > old_ets:
        graph.AddIntAttrDatN(nid, time_stamp, 'ets')

def update_ckf(graph, nid):
    ckf = graph.GetIntAttrDatN(nid, 'ckf')
    graph.AddIntAttrDatN(nid, ckf+1, 'ckf')

def add_node_attrs(graph, src_nid, dst_nid, time_range):
    graph.AddIntAttrDatN(src_nid, 1, 'ckf')
    graph.AddIntAttrDatN(dst_nid, 1, 'ckf')
    add_time_stamp(graph, src_nid, time_range[0])
    add_time_stamp(graph, dst_nid, time_range[1])

def update_node_attrs(graph, src_nid, dst_nid, time_range):
    update_ckf(graph, src_nid)
    update_ckf(graph, dst_nid)
    update_time_stamp(graph, src_nid, time_range[0])
    update_time_stamp(graph, dst_nid, time_range[1])

def add_edge_attrs(graph, src_nid, dst_nid, time_range):
    edge_id = graph.AddEdge(src_nid, dst_nid)
    graph.AddIntAttrDatE(edge_id, 1, 'freq')
    graph.AddFltAttrDatE(edge_id, int(time_range[1])-int(time_range[0]), 'duration')

def update_edge_attrs(graph, src_nid, dst_nid, time_range):
    edge_id = graph.GetEId(src_nid, dst_nid)
    freq = graph.GetIntAttrDatE(edge_id, 'freq')
    trsn_g.AddIntAttrDatE(edge_id, freq+1, 'freq')
    duration = graph.GetFltAttrDatE(edge_id, 'duration')
    new_duration = (duration + int(time_range[1]) - int(time_range[0])) / 2.0
    graph.AddFltAttrDatE(edge_id, new_duration, 'duration')

''' for each node in the graph, add two attributes
    1. two float values: latitude, longitute
    2. category
    3. parent-category
    '''
def add_category(graph, full_venue_dict, category_dict, pcategory_dict):
    for NI in graph.Nodes():
        vid = graph.GetStrAttrDatN(NI.GetId(), 'vid')
        if vid in full_venue_dict:
            graph.AddFltAttrDatN(NI.GetId(), float(full_venue_dict[vid]['lat']), 'lat')
            graph.AddFltAttrDatN(NI.GetId(), float(full_venue_dict[vid]['lng']), 'lng')
            graph.AddIntAttrDatN(NI.GetId(), category_dict[full_venue_dict[vid]['category']], 'category')
            graph.AddIntAttrDatN(NI.GetId(), pcategory_dict[full_venue_dict[vid]['parentcategory']], 'pcategory')




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
    Headache: Bug in DelNode()
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


