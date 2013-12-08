import snap
import Helper.GraphHelper as GH
import Helper.TimeHelper as TH
import Helper.VenueHelper as VH
import os, pickle


def create_vid_map(trsn_list):
    node_list = [item[0] for item in trsn_list]
    node_list.extend([item[1] for item in trsn_list])
    node_set = set(node_list)
    vid_map = {}

    #key: venue_id   val: node_id
    for nid, vid in enumerate(node_set):
        vid_map[vid] = nid
    return vid_map

def within_ts_range(sts, curr_ts):
    curr_ts = int(curr_ts)
    ets = sts + 3600*24*30 #hardcode 30 days
    if curr_ts >= sts and curr_ts < ets:
        return True
    else:
        return False


data_path = '../DataSet/Transition/'
graph_path = '../DataSet/GraphData/'
venue_path = '../DataSet/VenueData/'

trsn_list = VH.load_pickle_file(data_path, 'sf_trsn_small_new')
time_list = VH.load_pickle_file(data_path, 'sf_time_small_new')
full_venue_dict = VH.GetFullVenueDict(venue_path, 'venues-CA-new.json')
category_dict = VH.load_json(venue_path, 'category_map.json')
pcategory_dict = VH.load_json(venue_path, 'pcategory_map.json')

vid_map = create_vid_map(trsn_list)
ts_list = TH.gen_ts_list('201201010000', '201301010000', 30)

venue_g = snap.TNEANet.New()
for ts_idx, ts in enumerate(ts_list):
    for trsn_idx, trsn in enumerate(trsn_list):
        src_ts = time_list[trsn_idx][0] #only need check one ts
        dst_ts = time_list[trsn_idx][1]
        if (within_ts_range(ts, src_ts)):
            src_nid = vid_map[trsn[0]]
            dst_nid = vid_map[trsn[1]]
            GH.add_node(venue_g, src_nid, trsn[0], src_ts)
            GH.add_node(venue_g, dst_nid, trsn[1], dst_ts)
            GH.add_edge(venue_g, src_nid, dst_nid, time_list[trsn_idx])
    GH.add_category(venue_g, full_venue_dict, category_dict, pcategory_dict)
    print venue_g.GetNodes()
    GH.save_graph(venue_g, graph_path, 'sf_venue_small_'+ str(ts))
            


