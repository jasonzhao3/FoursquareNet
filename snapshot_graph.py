import snap
import Helper.GraphHelper as GH
import Helper.TimeHelper as TH
import Helper.VenueHelper as VH

print TH.gen_ts_list('201201010000', '201301010000', 30)

graph_path = '../DataSet/GraphData/'
venue_path = '../DataSet/VenueData/'
result_path = '../DataSet/Analysis/'
graph_name = 'sf_venue_graph'
category_name = 'category_map.json'
pcategory_name = 'pcategory_map.json'

# load graph and corresponding category_list
venue_g = GH.load_graph(graph_path, graph_name)
category_list = VH.get_category_list(venue_path, category_name)
print category_list
pcategory_list = VH.get_category_list(venue_path, pcategory_name)


edge_id = venue_g.GetEId(1,2)
print VH.get_category(venue_g, category_list, 1)
