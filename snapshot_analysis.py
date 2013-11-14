import snap
import Helper.GraphHelper as GH
import Helper.TimeHelper as TH
import Helper.VenueHelper as VH
import os, pickle
import matplotlib.pyplot as plt

snapshot_list = [ 'sf_venue_1325376000',
  'sf_venue_1327968000',
  'sf_venue_1330560000',
  'sf_venue_1333152000',
  'sf_venue_1335744000',
  'sf_venue_1338336000',
  'sf_venue_1340928000',
  'sf_venue_1343520000',
  'sf_venue_1346112000',
  'sf_venue_1348704000',
  'sf_venue_1351296000',
  'sf_venue_1353888000',
  'sf_venue_1356480000']

graph_path = '../DataSet/GraphData/'

# x: time
# y: total # of nodes in the graph
def generate_node_change():
  x, y = [], []
  for i in range(0, 13):
    filename = snapshot_list[i]
    g = GH.load_graph(graph_path, filename)
    print g.GetNodes()
    x.append(i)
    y.append(g.GetNodes())
  plt.plot(x, y, '-')
  plt.show()

# x: time
# y: delta(total # of edge in the graph) / delta(total weight of edge in graph) 
def generate_edge_ratio():
  x, y = [], []
  g = GH.load_graph(graph_path, snapshot_list[0])
  prev_nom, prev_denom = g.GetEdges(), 0.0
  for E in g.Edges():
    prev_denom += g.GetIntAttrDatE(E.GetId(), 'trsn_cnt')

  for i in range(1, 13):
    filename = snapshot_list[i]
    g = GH.load_graph(graph_path, filename)
    nom, denom = g.GetEdges(), 0.0
    for E in g.Edges():
      denom += g.GetIntAttrDatE(E.GetId(), 'trsn_cnt')
    x.append(i)
    y.append((nom-prev_nom) / (denom-prev_denom))
    prev_denom = denom
    prev_nom = nom

  plt.plot(x, y, '-')
  plt.show()

#generate_node_change()
generate_edge_ratio()
