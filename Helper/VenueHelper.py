import json
import os
import snap

def GetFullVenueDict(json_data_path, filename):
    src_file = os.path.join(json_data_path, filename)
    fin = open(src_file, 'r')
    venue_dict = dict()
    for line in fin:
        data = json.loads(line)
        venue_dict[data['id']] = data
    fin.close()
    return venue_dict


def build_category_dict(full_venue_dict):
    category_dict = {}
    pcategory_dict = {}
    cat_val = 0
    pcat_val = 0
    for vid, info in full_venue_dict.iteritems():
        category = info['category']
        pcategory = info['parentcategory']
        if category not in category_dict:
            category_dict[category] = cat_val
            cat_val += 1
        if pcategory not in pcategory_dict:
            pcategory_dict[pcategory] = pcat_val
            pcat_val += 1
    return category_dict, pcategory_dict

def load_json(data_path, filename):
    json_file = os.path.join(data_path, filename)
    json_data = open( json_file )
    json_dict = json.load( json_data )
    return json_dict


def dump_json(data_path, filename, json_dict):
    output_file = os.path.join(data_path, filename)
    with open( output_file, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4, separators=(',', ': '))

def get_category_list(data_path, filename):
    cate_dict = load_json(data_path, filename)
    key_vals = cate_dict.items()
    key_vals.sort(key=lambda t:t[1])
    return [item[0] for item in key_vals]

def get_category(graph, category_list, nid):
    idx = graph.GetIntAttrDatN(nid, 'category') 
    return category_list[idx]

def get_pcategory(graph, pcategory_list, nid):
    idx = graph.GetIntAttrDatN(nid, 'pcategory')
    return pcategory_list[idx]

# this file is amied to be called separately 
def save_category_map():
    data_path = '../DataSet/VenueData/'
    venue_file = 'venues-CA-new.json'
    category_file = 'category_map.json'
    pcategory_file = 'pcategory_map.json'
    full_venue_dict = GetFullVenueDict(data_path, venue_file)
    category_dict, pcategory_dict = build_category_dict(full_venue_dict)
    dump_json(data_path, category_file, category_dict)
    dump_json(data_path, pcategory_file, pcategory_dict)
    print "dump category map successfully!"
