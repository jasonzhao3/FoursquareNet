''' Deprecated -- can use build_snapshop_graph instead
'''

import snap
import os
import numpy as np
import Helper.GraphHelper as GH
import Helper.VenueHelper as VH
import pylab as plt
import json
import collections

graph_data_path = '../DataSet/GraphData/'
graph_filename = 'sf_trsn_graph'

venue_graph_data_path = '../DataSet/VenueData/'
venue_filename = 'venues-CA-new.json'

result_path = '../DataSet/Analysis/'

def GetFullVenueDict(json_data_path, filename):
  src_file = os.path.join(json_data_path, filename)
  fin = open(src_file, 'r')
  venue_dict = dict()
  for line in fin:
    data = json.loads(line)
    venue_dict[data['id']] = data
  fin.close()
  return venue_dict

# add attributes for graph nodes
def AddNodeAttr(graph, full_venue_dict):
  ''' for each node in the graph, add two attributes
      1. two float values: latitude, longitute
      2. category
      3. parent-category
  '''
  for NI in graph.Nodes():
    vid = graph.GetStrAttrDatN(NI.GetId(), 'vid')
    if vid in full_venue_dict:
      graph.AddFltAttrDatN(NI.GetId(), float(full_venue_dict[vid]['lat']), 'lat') 
      graph.AddFltAttrDatN(NI.GetId(), float(full_venue_dict[vid]['lng']), 'lng') 
      graph.AddStrAttrDatN(NI.GetId(), full_venue_dict[vid]['category'], 'category') 
      graph.AddStrAttrDatN(NI.GetId(), full_venue_dict[vid]['parentcategory'], 'pcategory') 
  #GH.save_graph(graph, result_path, result_filename)
  #return None

trsn_g = GH.load_graph(graph_data_path, graph_filename)
full_venue_dict = VH.GetFullVenueDict(venue_graph_data_path, venue_filename)
category_dict = VH.load_json(venue_graph_data_path, 'category_map.json')
pcategory_dict = VH.load_json(venue_graph_data_path, 'pcategory_map.json')

GH.add_category(trsn_g, full_venue_dict, category_dict, pcategory_dict)
GH.save_graph(trsn_g, graph_data_path, 'sf_venue_graph')
print 'successfully build venue_graph!'

