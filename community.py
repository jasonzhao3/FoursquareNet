import snap
import os
import numpy as np
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

data_path = '../CS224W_Dataset/GraphData'
filename = 'sf_trsn_graph_small'
trsn_g = GH.load_graph(data_path, filename)
un_trsn_g = to_PUNGraph(trsn_g)

# try to use the SNAP library function to get the community structure
# test_g = snap.GenRndGnm(snap.PUNGraph, 500, 1000)
communities = snap.TCnComV()
modularity = snap.CommunityGirvanNewman(un_trsn_g, communities)
print "done community detection."
for community in communities:
	print [node for node in community]
