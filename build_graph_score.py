''' In this cript, we will do a series of analysis,
    Just follow this template, build your own analysis script,
    and try to play with the graph :) '''

import snap
import os
import numpy as np
import Helper.GraphHelper as GH
import pylab as plt
import json
import collections

data_path = '../DataSet/GraphData/'
graph_filename = 'sf_trsn_graph'

json_data_path = '../DataSet/'
json_filename = 'venues-CA-new.json'

result_path = '../DataSet/Analysis/'
result_filename = 'sf_graph_with_attr'

# load graph first 
def LoadGraph(data_path, filename):
	graph_in = snap.TFIn(os.path.join(data_path, filename))
	trsn_g = snap.TNEANet.Load(graph_in)
	return trsn_g

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
  return None

trsn_g = LoadGraph(data_path, graph_filename)
full_venue_dict = GetFullVenueDict(json_data_path, json_filename)
AddNodeAttr(trsn_g, full_venue_dict)
