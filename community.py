import snap
import os
import json
import Helper.GraphHelper as GH

def to_PUNGraph(g):
	un_g = snap.TUNGraph.New()
	node_count = 0
	edge_count = 0
	for node in g.Nodes():
		node_count += 1
		un_g.AddNode(node.GetId())

	for edge in g.Edges():
		edge_count += 1
		un_g.AddEdge(edge.GetSrcNId(), edge.GetDstNId())

	print "node: %d edge: %d" % (node_count, edge_count)
	return un_g

def load_json(src_file):
    json_file = open(src_file)
    json_dict = json.load(json_file)
    json_file.close()
    return json_dict

def to_hash(venue_list):
	venue_hash = dict()
	for item in venue_list:
		venue_hash[item['id']] = [item['category'], item['venuename'], item['lat'], item['lng']]
	return venue_hash

data_path = '../CS224W_Dataset/GraphData'
filename = 'sf_trsn_graph_small'
trsn_g = GH.load_graph(data_path, filename)
un_trsn_g = to_PUNGraph(trsn_g)

# try to use the SNAP library function to get the community structure
# communities = snap.TCnComV()
# modularity = snap.CommunityCNM(un_trsn_g, communities)
# print "Community detection complete, modularity score is", modularity
# for community in communities:
# 	print [node for node in community]
communities = [[46, 2377, 3016], [260, 1442, 1988, 4536], [684, 974, 3056, 6266]]

# fetch venue info and produce a csv for visualization
data_path = '../CS224W_Dataset'
src_file = os.path.join(data_path, 'venues-CA-new.json')
venue_list = load_json(src_file)
# transform the venue list to a hash
venue_hash = to_hash(venue_list)

for i in range(len(communities)):
	for nodeID in communities[i]:
		vid = trsn_g.GetStrAttrDatN(nodeID, 'vid')
		print venue_hash[vid][1]

