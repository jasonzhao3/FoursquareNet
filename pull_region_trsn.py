'''
    This script is used to pull region transition data from the original transition file(1.5GB).
    Based on the json file(e.g. 'venues-CA-vis.json'), we can get the venue_id of venues in certain area(e.g. San Francisco'). Then we parse the original transition data using these venue_ids. Whenever a transition happens to the venue within this area, we pull it out.
    The output is the transition file for a certain region. '''


import json
import os, pickle
import Helper.GraphHelper as GH
import Helper.VenueHelper as VH

data_path = '../DataSet/'
venue_path = '../DataSet/VenueData'
trsn_path = '../DataSet/Transition'

def load_json(src_file):
    json_file = open(src_file)
    json_dict = json.load(json_file)
    json_file.close()
    return json_dict


def dump_trsn_time(src_file, out_trsn, out_time):
    trsn_list = []
    time_list = []
    with open(src_file) as f:
        for line in f:
            attr_list = line.split('\t')
            # be more strict -- trsn start and end both in SF
            if attr_list[0] in region_id_set and attr_list[2] in region_id_set:
                trsn_list.append((attr_list[0], attr_list[2]))
                time_list.append((attr_list[1], attr_list[3]))
                print "add another "+ attr_list[0]
    
    out_trsn = open(out_trsn, 'wb')
    out_time = open(out_time, 'wb')
    pickle.dump(trsn_list, out_trsn)
    pickle.dump(time_list, out_time)
    out_trsn.close()
    out_time.close()

'''deprecated venues-CA-vis.json
src_file = os.path.join(data_path, 'venues-CA-vis.json')
venue_list = load_json(src_file)
print venue_list[0]

region_name = 'San Francisco'
region_id_list = [item['id'] for item in venue_list if item['city'] == region_name]
region_id_set = set(region_id_list)


'''
full_venue_dict = VH.GetFullVenueDict(venue_path, 'venues-CA-new.json')

region_name = 'San Francisco'
region_id_set = set()
for vid, data in full_venue_dict.iteritems():
    if data['city'] == region_name:
        region_id_set.add(vid)

#chekin_files are small files split from the 1.5GB file
alpha_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
prefix = 'checkin_seg_a'
checkin_files = []
for alpha in alpha_list:
    checkin_files.append(prefix+alpha)

for file_name in checkin_files:
    src_file = os.path.join(data_path, file_name)
    out_trsn = os.path.join(trsn_path, 'out_trsn_' + file_name)
    out_time = os.path.join(trsn_path, 'out_time_' + file_name)
    dump_trsn_time(src_file, out_trsn, out_time)
    print "successfully dump " + file_name

 
