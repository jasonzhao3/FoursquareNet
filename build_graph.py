import snap
import os, pickle

data_path = '../DataSet/'
trsn_file = open(os.path.join(data_path, 'sf_trsn'))
#time_file = open(os.path.join(data_path, 'sf_time'))


trsn_list = pickle.load(trsn_file)
#time_list = pickle.load(time_file)

node_list = [item[0] for item in trsn_list]
node_list.extend([item[1] for item in trsn_list])
node_set = set(node_list)
node_hash = {}

#key: venue_id   val: node_id
nid = 0
for venue_id in node_set:
    node_hash[venue_id] = nid
    nid += 1

trsn_g = snap.TNEANet.New()
#node_id: 0 to n-1
for nid in xrange(len(node_set)):
    trsn_g.AddNode(nid)
#freq: frequncy(cnt) of edge
print trsn_g.GetNodes()
for trsn in trsn_list:
    src_nid = node_hash[trsn[0]]
    dest_nid = node_hash[trsn[1]]
    print src_nid, dest_nid
    if not trsn_g.IsEdge(src_nid, dest_nid):
        print "begin add node"
        edge_id = trsn_g.AddEdge(src_nid, dest_nid)
        trsn_g.AddIntAttrDatE(edge_id, 1, 'freq')  
        print "add a new edge, hoho~"
    else:
        edge_id = trsn_g.GetEId(src_nid, dest_nid)
        freq = trsn_g.GetIntAttrDatE(edge_id, 'freq')
        trsn_g.AddIntAttrDatE(edge_id, freq+1, 'freq')
        print "update edge frequency to %d !" %(freq)

trsn_graph = os.path.join(data_path, 'sf_trsn_graph')
graph_out = snap.TFOut(trsn_graph)
trsn_g.Save(graph_out)
graph_out.Flush()
print "succesfully build the graph!"





