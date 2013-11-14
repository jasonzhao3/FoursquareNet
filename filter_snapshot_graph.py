import snap
import Helper.GraphHelper as GH
import Helper.TimeHelper as TH
import Helper.VenueHelper as VH

# file configuration
# TODO: create a configuration module
graph_path = '../DataSet/GraphData/'
venue_path = '../DataSet/VenueData/'
result_path = '../DataSet/Analysis/'
graph_name = 'sf_venue_graph'
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
ts_list = TH.gen_ts_list('201201010000', '201301010000', 30)
ts_list.reverse()
for ts in ts_list:
    GH.filter_node_sts(venue_g, ts)
    GH.save_graph(venue_g, graph_path, 'sf_venue_'+ts)



