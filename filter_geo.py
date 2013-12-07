import snap
import Helper.GraphHelper as GH
import Helper.TimeHelper as TH
import Helper.VenueHelper as VH

# file configuration
# TODO: create a configuration module
graph_path = '../DataSet/GraphData/'
venue_path = '../DataSet/VenueData/'
result_path = '../DataSet/Analysis/'
#graph_name = 'sf_venue_graph'
graph_name = 'sf_venue_center'
category_name = 'category_map.json'
pcategory_name = 'pcategory_map.json'

# load graph and corresponding category_list
'''
    Currently, the graph has node attribute:
    - vid
    - ckn (insofar, checkin number)
    - sts (start timestamp)
    - ets (end timestamp)
    - lat
    - lng
    - category
    - pcategor
    
    And edge attribute:
    - trsn_cnt
    - duration
'''
venue_g = GH.load_graph(graph_path, graph_name)
category_list = VH.get_category_list(venue_path, category_name)
pcategory_list = VH.get_category_list(venue_path, pcategory_name)
#GH.print_node_attr_names(venue_g)
#GH.print_edge_attr_names(venue_g)
#print category_list
GH.print_nids(venue_g)


# create snapshop of the graph - node accurate, but edge aren't
center = (37.76010, -122.44779)
radius = 0.095
print venue_g.GetNodes()
print venue_g.GetEdges()
i = 0
for edge in venue_g.Edges():
    i += 1
    print venue_g.GetIntAttrDatE(edge.GetId(), 'trsn_cnt'), i
GH.filter_node_geo(venue_g, center, radius)
print venue_g.GetNodes()
#GH.save_graph(venue_g, graph_path, 'sf_venue_center')



