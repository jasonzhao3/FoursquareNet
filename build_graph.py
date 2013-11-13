'''
    This script is used to build our first transition graph.
    We use TNEANet with node attributes and edge attribues.
    For details of the graph structure, please refer the google doc - milestone.
'''

import snap
import os, pickle

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
    ckf = trsn_g.GetIntAttrDatN(nid, 'ckf')
    trsn_g.AddIntAttrDatN(nid, ckf+1, 'ckf')

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



data_path = '../DataSet/'
graph_path = '../DataSet/GraphData/'
trsn_file = open(os.path.join(data_path, 'sf_trsn'))
time_file = open(os.path.join(data_path, 'sf_time'))
trsn_list = pickle.load(trsn_file)
time_list = pickle.load(time_file)

#trsn_file = open(os.path.join(data_path, 'sf_trsn_small'))
#time_file = open(os.path.join(data_path, 'sf_time_small'))
#trsn_list = pickle.load(trsn_file)
#time_list = pickle.load(time_file)

node_list = [item[0] for item in trsn_list]
node_list.extend([item[1] for item in trsn_list])
node_set = set(node_list)
node_hash = {}

#key: venue_id   val: node_id
#TODO: add timestamp filter
for nid, vid in enumerate(node_set):
    node_hash[vid] = nid

trsn_g = snap.TNEANet.New()
#node_id: 0 to n-1
for vid, nid in node_hash.iteritems():
    trsn_g.AddNode(nid)
    trsn_g.AddStrAttrDatN(nid, vid, 'vid')

#freq: frequncy(cnt) of edge
print trsn_g.GetNodes()
for idx, trsn in enumerate(trsn_list):
    src_nid = node_hash[trsn[0]]
    dst_nid = node_hash[trsn[1]]
    print src_nid, dst_nid
    #TODO: add timestamp filter
    if not trsn_g.IsEdge(src_nid, dst_nid):
        add_edge_attrs(trsn_g, src_nid, dst_nid, time_list[idx])
        add_node_attrs(trsn_g, src_nid, dst_nid, time_list[idx])
        print "add a new edge, hoho~"
    else:
        update_edge_attrs(trsn_g, src_nid, dst_nid, time_list[idx])
        update_node_attrs(trsn_g, src_nid, dst_nid, time_list[idx])
        print "update node info, haha~"
    print idx, trsn
    print len(trsn_list)    

GH.save_graph(trsn_g, graph_path, 'sf_trsn_graph')
print "succesfully build the graph!"

