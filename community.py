import snap, os, json, csv
import Helper.GraphHelper as GH
import Helper.VenueHelper as VH

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
communities = snap.TCnComV()
modularity = snap.CommunityCNM(un_trsn_g, communities)
print "Community detection complete, modularity score is", modularity
# communities = [[3280, 2414, 2662, 2878, 3551], [848, 1106, 1474, 1915, 2089, 3139, 3400, 5759, 6280, 7848]]

# fetch venue info and produce a csv for visualization
data_path = '../CS224W_Dataset'
out_csv = '../CS224W_Dataset/Community/transition-SF-community.csv'
venue_hash = VH.GetFullVenueDict(data_path, 'venues-CA-new.json')

with open(out_csv, 'w') as fout:
	a = csv.writer(fout, delimiter=',', quoting=csv.QUOTE_ALL)
	a.writerow(['venuename', 'community', 'category', 'parentcategory', 'lat', 'lng'])
	for i in range(communities.Len()):
		for nodeID in communities[i]:
			vid = trsn_g.GetStrAttrDatN(nodeID, 'vid')
			if(vid in venue_hash):
				venue_data = venue_hash[vid]
				data_to_write = [venue_data['venuename'], str(i), venue_data['category'], venue_data['parentcategory'], venue_data['lat'], venue_data['lng']]
				a.writerow([d.encode('utf8') for d in data_to_write])




