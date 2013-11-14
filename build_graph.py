'''
    This script is used to build our first transition graph.
    We use TNEANet with node attributes and edge attribues.
    For details of the graph structure, please refer the google doc - milestone.
'''

import snap
import os, pickle
import Helper.GraphHelper as GH


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
        GH.add_edge_attrs(trsn_g, src_nid, dst_nid, time_list[idx])
        GH.add_node_attrs(trsn_g, src_nid, dst_nid, time_list[idx])
        print "add a new edge, hoho~"
    else:
        GH.update_edge_attrs(trsn_g, src_nid, dst_nid, time_list[idx])
        GH.update_node_attrs(trsn_g, src_nid, dst_nid, time_list[idx])
        print "update node info, haha~"
    print idx, trsn
    print len(trsn_list)    

GH.save_graph(trsn_g, graph_path, 'sf_trsn_graph')
print "succesfully build the graph!"

