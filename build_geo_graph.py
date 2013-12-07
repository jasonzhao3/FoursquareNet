import snap
import Helper.GraphHelper as GH
import Helper.TimeHelper as TH
import Helper.VenueHelper as VH
import os, pickle

center = (37.76010, -122.44779)
radius = 0.095

def create_vid_map(trsn_list):
    node_list = [item[0] for item in trsn_list]
    node_list.extend([item[1] for item in trsn_list])
    node_set = set(node_list)
    vid_map = {}

    #key: venue_id   val: node_id
    for nid, vid in enumerate(node_set):
        vid_map[vid] = nid
    return vid_map


def within_geo_range(center, radius, lat, lng):
    c_lat = center[0]
    c_lng = center[1]
#    print lat, c_lat, lng, c_lng
#    print abs(lat-c_lat), abs(lng-c_lng)
    if abs(lat-c_lat) <= radius and abs(lng-c_lng) <= radius:
        return True
    else:
        print "catch a false"
        return False
    

data_path = '../DataSet/'
graph_path = '../DataSet/GraphData/'
venue_path = '../DataSet/VenueData/'

trsn_list = VH.load_pickle_file(data_path, 'sf_trsn')
time_list = VH.load_pickle_file(data_path, 'sf_time')

full_venue_dict = VH.GetFullVenueDict(venue_path, 'venues-CA-new.json')
category_dict = VH.load_json(venue_path, 'category_map.json')
pcategory_dict = VH.load_json(venue_path, 'pcategory_map.json')
lng_list = [GH.get_lat_lng(full_venue_dict, trsn[1]) for trsn in trsn_list]
print max(lng_list)

'''
vid_map = create_vid_map(trsn_list)

venue_g = snap.TNEANet.New()
lngs = []
for trsn_idx, trsn in enumerate(trsn_list):
    # only need check one vid
    lat, lng = GH.get_lat_lng(full_venue_dict, trsn[0])
    if within_geo_range(center, radius, lat, lng):
        lngs.append(lng)
        src_nid = vid_map[trsn[0]]
        dst_nid = vid_map[trsn[1]]
        src_ts = time_list[trsn_idx][0]
        dst_ts = time_list[trsn_idx][1]
        GH.add_node(venue_g, src_nid, trsn[0], src_ts)
        GH.add_node(venue_g, dst_nid, trsn[1], dst_ts)
        GH.add_edge(venue_g, src_nid, dst_nid, time_list[trsn_idx])
#        print "add one more node!"
GH.add_category(venue_g, full_venue_dict, category_dict, pcategory_dict)
print venue_g.GetNodes()
print max(lngs)
GH.save_graph(venue_g, graph_path, 'sf_venue_center')

undirected_g = GH.convert_undirected_graph(venue_g)
GH.save_graph(undirected_g, graph_path, 'sf_venue_center_undirected')
'''        


