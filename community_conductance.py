import snap, os, json, csv
import Helper.GraphHelper as GH
import Helper.VenueHelper as VH

def create_weight_hash(G):
	weight_hash = dict()

	for edge in G.Edges():
		weight_hash[(edge.GetSrcNId(), edge.GetDstNId())] = G.GetIntAttrDatE(edge.GetId(), 'trsn_cnt')

	return weight_hash

def create_undirected(G):
	un_g = snap.TUNGraph.New()
	node_count = 0
	edge_count = 0
	for node in G.Nodes():
		node_count += 1
		un_g.AddNode(node.GetId())

	for edge in G.Edges():
		edge_count += 1
		un_g.AddEdge(edge.GetSrcNId(), edge.GetDstNId())

	# print "node: %d edge: %d" % (node_count, edge_count)
	return un_g

def create_degree_hash(G):
	degree_hash = dict()
	for node in G.Nodes():
		node_id = node.GetId()
		degree_hash[node_id] = G.GetIntAttrDatN(node_id, 'ckn')

	return degree_hash

def get_directed_weight(weight_hash, UG, node_1, node_2):
	if(not UG.IsEdge(node_1, node_2)):
		return 0

	weight = 0
	if((node_1, node_2) in weight_hash):
		weight += weight_hash[(node_1, node_2)]
	if((node_2, node_1) in weight_hash):
		weight += weight_hash[(node_2, node_1)]
	return weight

def get_max_weighted_edge_ends(weight_hash, UG):
	max_weight = 0
	max_src = 0
	max_dst = 0
	for e in UG.Edges():
		weight = get_directed_weight(weight_hash, UG, e.GetSrcNId(), e.GetDstNId())
		if(weight > max_weight):
			max_weight = weight
			max_src = e.GetSrcNId()
			max_dst = e.GetDstNId()
	print "max_weight", max_weight
	return [max_src, max_dst]

def get_neighbors(UG, nodeIDs):
	neighbors = set()
	for node_id in nodeIDs:
		node = UG.GetNI(node_id)
		for another_id in node.GetOutEdges():
			neighbors.add(another_id)
	return list(neighbors)

def get_max_belonging_degree(weight_hash, UG, neighbors, community, degree_hash):
	max_belonging_degree = 0
	max_node = 0
	for node_id in neighbors:
		weight_sum = 0
		belonging_degree = 0
		for in_node in community:
			weight = get_directed_weight(weight_hash, UG, node_id, in_node)
			weight_sum += weight
		degree = degree_hash[node_id]
		belonging_degree = float(weight_sum)/degree
		if(belonging_degree > max_belonging_degree):
			max_belonging_degree = belonging_degree
			max_node = node_id
	return node_id

def get_conductance(weight_hash, UG, community):
	cut_edges_weights = 0
	in_community_weights = 0
	for in_node_id in community:
		in_node = UG.GetNI(in_node_id)
		for neighbor_id in in_node.GetOutEdges():
			if(not neighbor_id in community):
				weight = get_directed_weight(weight_hash, UG, in_node_id, neighbor_id)
				cut_edges_weights += weight
			else:
				weight = get_directed_weight(weight_hash, UG, in_node_id, neighbor_id)
				in_community_weights += weight
	in_community_weights = in_community_weights/2
	return (cut_edges_weights)/float(in_community_weights + cut_edges_weights)

def delete_edges(UG, community):
	for node_id1 in community:
		for node_id2 in community:
			if(UG.IsEdge(node_id1, node_id2)):
				UG.DelEdge(node_id1, node_id2)

def detect_community(weight_hash, UG, degree_hash):
	communities = []

	while(UG.GetEdges() != 0):
		community = get_max_weighted_edge_ends(weight_hash, UG)
		neighbors = get_neighbors(UG, community)
		
		while(len(neighbors) != 0):
			print "inner loop!!"
			neighbors = get_neighbors(UG, community)
			updated_community = list(community)
			updated_community.append(get_max_belonging_degree(weight_hash, UG, neighbors, community, degree_hash))

			if(get_conductance(weight_hash, UG, updated_community) < get_conductance(weight_hash, UG, community)):
				community = updated_community
			else:
				break

		print "Conductance", get_conductance(weight_hash, UG, community)
		print "community detected!", len(communities)
		delete_edges(UG, community)
		communities.append(community)

	return communities

def main():
	data_path = '../CS224W_Dataset/GraphData'
	filename = 'sf_venue_center_small'
	venue_g = GH.load_graph(data_path, filename)
	weight_hash = create_weight_hash(venue_g)
	degree_hash = create_degree_hash(venue_g)
	un_venue_g = create_undirected(venue_g)
	print "start community detection"
	communities = detect_community(weight_hash, un_venue_g, degree_hash)
	print communities

if __name__ == '__main__':
  main()