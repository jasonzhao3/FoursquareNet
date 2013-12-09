import collections
import os
import numpy as np
import pylab as plt

import snap
import Helper.GraphHelper as GH
import Helper.AnalysisHelper as AH

DIR_PATH = '../DataSet/GraphData/'
FILE_PREFIX = 'sf_venue_1'


# SF_VENUE_GRAGH_NAME = 'sf_venue_graph'
RES_PATH = '../predict_output/'
RES_PREFIX = 'monthly_predict_naive_'
RES_SUFFIX = '.png'

# global variables for page rank
ITER_THRESHOLD = 30
CHANGE_THRESHOLD = 100
BETA = 1.0 
ORI_FACTOR = 1 
MUL_FACTOR = 2 

# TRANS_PATH = '../DataSet/TransGraphData/'
# TRANS_FILE_PREFIX = 'trans_graph_'
TRANS_PATH = '../DataSet/TransEnhancedGraphData/' + str(MUL_FACTOR) + '/'
TRANS_FILE_PREFIX = 'trans_graph_enhanced_'
#TRANS_PATH = '../DataSet/TransEnhancedGraphData/dynamic/'
#TRANS_FILE_PREFIX = 'trans_graph_enhanced_'

def get_monthly_venue_graphs():
  files = os.listdir(DIR_PATH)
  file_month_list = []
  for fn in files:
    if fn.startswith(FILE_PREFIX):
      file_month_list.append(fn)
  return [GH.load_graph(DIR_PATH, fn) for fn in file_month_list]

def get_node_list(G):
  return [NI.GetId() for NI in G.Nodes()]

def show_plot(xlabel, ylabel, xlog=False, ylog=False):
  plt.xscale('log') if xlog else None
  plt.yscale('log') if ylog else None
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.subplot(111).legend()
  plt.show()


# naive prediction based on previous check-in frequency
def predict_naive(G, total_ckn_inc):
  ckn_cntr = collections.Counter()
  for node in G.Nodes():
    ckn_cntr[node.GetId()] = G.GetIntAttrDatN(node.GetId(), 'ckn')
  total = sum(ckn_cntr.values())
  for nid in ckn_cntr:
    ckn_cntr[nid] = float(total_ckn_inc) * ckn_cntr[nid]/total

  return ckn_cntr


# prediction by pagerank with teleporting for dead ends
def predict_pagerank_naive(G, total_ckn_inc):
  init_value = float(total_ckn_inc) / G.GetNodes()
  ckn_cntr = collections.Counter()
  
  for node in G.Nodes():
    ckn_cntr[node.GetId()] = init_value
  
  limit = ITER_THRESHOLD 
  c = 0
  teleport_const = (1 - BETA) * total_ckn_inc / G.GetNodes()

  total_changed = 10000
  # start page rank
  while (total_changed > CHANGE_THRESHOLD) and (c < limit):
    old_cntr = ckn_cntr
    ckn_cntr = collections.Counter()
    add_on_value = 0.0
    
    dead_end_cnt = 0
    for u in G.Nodes():
      uid = u.GetId()
      out_degree_cntr = collections.Counter()
      for vid in u.GetOutEdges():
        eid = G.GetEId(uid, vid)
        out_degree_cntr[vid] = G.GetIntAttrDatE(eid, 'trsn_cnt')
      total_out_deg = sum(out_degree_cntr.values())

      # for dead ends:
      if total_out_deg == 0:
        add_on_value += float(old_cntr[uid]) / G.GetNodes()
        dead_end_cnt += 1
        continue

      for vid in out_degree_cntr:
        ckn_cntr[vid] += BETA*(float(old_cntr[uid]) * out_degree_cntr[vid]/total_out_deg)

    # print ">> iteration: ", c
    # print "   - count dead end: ", dead_end_cnt, " total: ", G.GetNodes()
    for v in G.Nodes():
      ckn_cntr[v.GetId()] += add_on_value
    # for u in G.Nodes():
      # ckn_cntr[u.GetId()] += teleport_const 
    
    total_changed = 0.0
    for u in G.Nodes():
      uid = u.GetId()
      total_changed += abs(ckn_cntr[uid] - old_cntr[uid])
    # print "   ??? decreased ??? ", sum(old_cntr.values()), " >> ", sum(ckn_cntr.values())
    # print "   total changed ckn: ", total_changed
    c += 1

  print "   iteration: ", c
  # for node in G.Nodes():
  #   nid = node.GetId()
  #   ckn_cntr[nid] += G.GetIntAttrDatN(nid, 'ckn')
  return ckn_cntr

def compare_ckn(G, G_next, predicted_ckn, idx):
  pred_dict = collections.Counter() 
  gold_dict = collections.Counter()

  for node in G_next.Nodes():
    nid = node.GetId()
    gold_dict[nid] += G_next.GetIntAttrDatN(nid, 'ckn')
    pred_dict[nid] = 0.0

  for node in G.Nodes():
    nid = node.GetId()
    gold_dict[nid] -= G.GetIntAttrDatN(nid, 'ckn')
    pred_dict[nid] += predicted_ckn[nid]

  gold_list = []
  pred_list = []
  for node in G_next.Nodes():
    nid = node.GetId()
    gold_list.append(gold_dict[nid])
    pred_list.append(pred_dict[nid])

  diff_list = [pred_list[idx] - gold_list[idx] for idx in range(0, G_next.GetNodes())]
  print "    mean: ", np.mean(diff_list)
  print "    std : ", np.std(diff_list)

  F_score = sum([diff*diff for diff in diff_list]) * 1.0 / sum(gold_list)
  abs_diff_list = [abs(v) for v in diff_list]
  print "    off by: ", float(sum(abs_diff_list))/sum(gold_list)
  print "F score: ", F_score

  sorted_pair = [(gold_list[idx], pred_list[idx]) for idx in range(0, G_next.GetNodes())]
  sorted_pair = sorted(sorted_pair, reverse=True)

  sorted_gold = [p[0] for p in sorted_pair]
  sorted_pred = [p[1] for p in sorted_pair]
  plt.plot(range(0, G_next.GetNodes()), sorted_pred, color='red')
  plt.plot(range(0, G_next.GetNodes()), sorted_gold, color='blue')
  show_plot("venue", "check-in number", xlog=True)
  #plt.savefig(os.path.join(RES_PATH, RES_PREFIX + str(idx) + RES_SUFFIX))

def get_node_increase_list(G_list):
  res = []
  for idx in range(1, len(G_list)):
    res.append(G_list[idx].GetNodes() - G_list[idx-1].GetNodes())
  return res

def get_ckn_from_graph(G):
  return sum([G.GetIntAttrDatN(node.GetId(), 'ckn') for node in G.Nodes()])

def get_ckn_total_increase_list(G_list):
  res = []
  for idx in range(1, len(G_list)):
    diff = get_ckn_from_graph(G_list[idx]) - get_ckn_from_graph(G_list[idx-1])
    res.append(diff)
  return res

def predict_with_cur_and_new_nodes(G, new_node_list):
  place_holder = 1

# modify the edge weight graphs in second list to reflect monthly transitions 
def generate_monthly_trans_graphs():
  graphs = get_monthly_venue_graphs()
  for idx in range(len(graphs)-1, 0, -1):
    cur_graph = graphs[idx]
    prev_graph = graphs[idx-1]
    for edge in prev_graph.Edges():
      src_nid = edge.GetSrcNId()
      dst_nid = edge.GetDstNId()

      cur_eid = cur_graph.GetEId(src_nid, dst_nid)
      cur_weight = cur_graph.GetIntAttrDatE(cur_eid, 'trsn_cnt')
      prev_eid = prev_graph.GetEId(src_nid, dst_nid)
      prev_weight = prev_graph.GetIntAttrDatE(prev_eid, 'trsn_cnt')

      diff = cur_weight - prev_weight
      # cur_graph.AddIntAttrDatE(cur_eid, cur_weight - prev_weight, 'trsn_cnt')
      month_coeff = float(idx)
      cur_graph.AddIntAttrDatE(cur_eid, ORI_FACTOR*cur_weight + month_coeff*MUL_FACTOR*diff, 'trsn_cnt')
    print "updated trans graph for month ", idx

  for idx, G in enumerate(graphs):
    idx_str = str(idx) if idx < 10 else '9'+str(idx)
    GH.save_graph(G, TRANS_PATH, TRANS_FILE_PREFIX + idx_str)

def get_monthly_trans_graphs():
  files = os.listdir(TRANS_PATH)
  file_month_list = []
  for fn in files:
    if not fn.endswith('DS_Store'):
      file_month_list.append(fn)
  return [GH.load_graph(TRANS_PATH, fn) for fn in file_month_list]

if __name__ == '__main__':
  # load 13 monthly graphs from files
  monthly_graphs = get_monthly_venue_graphs() 
  # generate_monthly_trans_graphs()
  monthly_graphs_trans = get_monthly_trans_graphs()

  print "===== finished loading graphs ====="
  print "\n"
  # get some high-level data about each month
  node_inc_list = get_node_increase_list(monthly_graphs)
  ckn_total_inc_list = get_ckn_total_increase_list(monthly_graphs)

  # plt.plot(range(0, len(node_inc_list)), node_inc_list)  
  # show_plot("month", "node increase")
  # plt.plot(range(0, len(ckn_total_inc_list)), ckn_total_inc_list)
  # show_plot("month", "check-in increase")
 
  predict_indices = range(9, 12) # almost range(0, 12)

  for idx in predict_indices:
    # cur_graph = monthly_graphs[idx]
    cur_graph = monthly_graphs_trans[idx]

    print "===== predict %d-th month" % (idx+1)
    
    # pred_ckn = predict_naive(cur_graph, ckn_total_inc_list[idx])
    pred_ckn = predict_pagerank_naive(cur_graph, ckn_total_inc_list[idx])
    gold_graph = monthly_graphs[idx+1]
    compare_ckn(cur_graph, gold_graph, pred_ckn, idx)
  # cur_graph = monthly_graphs[1]
  # next_graph = monthly_graphs[2]

  # predict_with_cur_only(cur_graph)
  # 
  # new_node_list = get_node_list(next_graph)
  # predict_with_cur_and_new_nodes(cur_graph, new_node_list)
  


