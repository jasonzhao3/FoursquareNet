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

#TRANS_PATH = '../DataSet/TransGraphData/'
#TRANS_FILE_PREFIX = 'trans_graph_'
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

# get the distribution of check-in increase of current month(vs. previous month)
def get_node_dist(G, prev_G):
  ckn_cntr = collections.Counter()
  for node in G.Nodes():
    ckn_cntr[node.GetId()] = G.GetIntAttrDatN(node.GetId(), 'ckn')
    # if prev_G != None and prev_G.IsNode(node.GetId()):
    #   ckn_cntr[node.GetId()] -= prev_G.GetIntAttrDatN(node.GetId(), 'ckn')
  total = sum(ckn_cntr.values())
  for nid in ckn_cntr:
    ckn_cntr[nid] = float(ckn_cntr[nid])/total
  return ckn_cntr

# prediction by pagerank with prev. distribution info
SMOOTH_COEFF = 0.005 
def predict_pagerank_with_dist_learn(G, total_ckn_inc, dist, learn_dict):
  SMOOTH_COEFF = 150.0 / G.GetNodes()
  print "smooth coeff: ", SMOOTH_COEFF

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
        # change the weight distribution to reflect previous distribution info
        learn_coeff = 1.0 if learn_dict == None or learn_dict[vid] == 0 else learn_dict[vid]
        out_degree_cntr[vid] = learn_coeff * G.GetIntAttrDatE(eid, 'trsn_cnt') * (SMOOTH_COEFF+dist[vid])
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

def predict_pagerank_with_dist(G, total_ckn_inc, dist):
  SMOOTH_COEFF = 150.0 / G.GetNodes()
  print "smooth coeff: ", SMOOTH_COEFF

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
        # change the weight distribution to reflect previous distribution info
        out_degree_cntr[vid] = G.GetIntAttrDatE(eid, 'trsn_cnt') * (SMOOTH_COEFF+dist[vid])
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

def predict_pagerank_new_nodes(G, new_node_list, total_ckn_inc):
  numOfNodes = len(new_node_list)

  init_value = float(total_ckn_inc) / numOfNodes 
  ckn_cntr = collections.Counter()
  
  for nid in new_node_list:
    ckn_cntr[nid] = init_value
  
  limit = ITER_THRESHOLD 
  c = 0

  total_changed = 10000
  # start page rank
  while (total_changed > CHANGE_THRESHOLD) and (c < limit):
    old_cntr = ckn_cntr
    ckn_cntr = collections.Counter()
    add_on_value = 0.0
    
    dead_end_cnt = 0
    for uid in new_node_list:
      out_degree_cntr = collections.Counter()
      total_out_deg = 0

      # if u is a node in the current graph
      if G.IsNode(uid):
        u = G.GetNI(uid)
        for vid in u.GetOutEdges():
          eid = G.GetEId(uid, vid)
          out_degree_cntr[vid] = G.GetIntAttrDatE(eid, 'trsn_cnt')
        total_out_deg = sum(out_degree_cntr.values())

      # for new incoming nodes and dead ends:
      if total_out_deg == 0:
        add_on_value += float(old_cntr[uid]) / numOfNodes 
        dead_end_cnt += 1
        continue

      for vid in out_degree_cntr:
        ckn_cntr[vid] += BETA*(float(old_cntr[uid]) * out_degree_cntr[vid]/total_out_deg)

    for vid in new_node_list:
      ckn_cntr[vid] += add_on_value
    
    total_changed = 0.0
    for uid in new_node_list:
      total_changed += abs(ckn_cntr[uid] - old_cntr[uid])
    # print "   ??? decreased ??? ", sum(old_cntr.values()), " >> ", sum(ckn_cntr.values())
    # print "   total changed ckn: ", total_changed
    c += 1

  print "   iteration: ", c
  return ckn_cntr


def compare_ckn(G, G_next, predicted_ckn, idx):
  pred_dict = collections.Counter() 
  gold_dict = collections.Counter()

  learn_dict = collections.Counter()
  
  # only compare the nodes in previous graph
  for node in G.Nodes():
    nid = node.GetId()
    # gold_dict[nid] -= G.GetIntAttrDatN(nid, 'ckn')
    gold_dict[nid] = G_next.GetIntAttrDatN(nid, 'ckn') - G.GetIntAttrDatN(nid, 'ckn')
    pred_dict[nid] = predicted_ckn[nid]
    if gold_dict[nid] > 0 and pred_dict[nid] > 0:
      #learn_dict[nid] = float(gold_dict[nid])/pred_dict[nid]
      if gold_dict[nid] > pred_dict[nid]: learn_dict[nid] = 1.1 
      else: learn_dict[nid] = 0.9
    else:
      learn_dict[nid] = 1.0

  gold_list = []
  pred_list = []
  for node in G_next.Nodes():
    nid = node.GetId()
    gold_list.append(gold_dict[nid])
    pred_list.append(pred_dict[nid])


  sorted_pair = [(gold_list[idx], pred_list[idx]) for idx in range(0, G_next.GetNodes())]
  sorted_pair = sorted(sorted_pair, reverse=True)

  sorted_gold = [p[0] for p in sorted_pair]
  sorted_pred = [p[1] for p in sorted_pair]
  
  # numOfNodes = G_next.GetNodes()
  numOfNodes = 10 
  diff_list = [sorted_pred[idx] - sorted_gold[idx] for idx in range(0, numOfNodes)]
  print "    mean: ", np.mean(diff_list)
  print "    std : ", np.std(diff_list)

  F_score = sum([diff*diff for diff in diff_list]) * 1.0 / sum(sorted_gold[0:numOfNodes])
  abs_diff_list = [abs(v) for v in diff_list]
  print "    off by: ", float(sum(abs_diff_list))/sum(sorted_gold[0:numOfNodes])
  print "F score: ", F_score
 
  succ_cnt = 0.0
  for idx in range(0, numOfNodes):
    if abs_diff_list[idx]/sorted_gold[idx] < 0.2:
      succ_cnt += 1
  print "Succ rate: ", succ_cnt
  # plt.plot(range(0, G_next.GetNodes()), sorted_pred, color='red')
  # plt.plot(range(0, G_next.GetNodes()), sorted_gold, color='blue')
  # show_plot("venue", "check-in number", xlog=True)
  
  #plt.plot(range(0, numOfNodes), sorted_pred[0:numOfNodes], color='red')
  #plt.plot(range(0, numOfNodes), sorted_gold[0:numOfNodes], color='blue')
  #show_plot("venue(first 100)", "check-in number")
  
  #plt.savefig(os.path.join(RES_PATH, RES_PREFIX + str(idx) + RES_SUFFIX))
  return learn_dict

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

def get_ckn_total_increase_list_cur(G_list):
  res = []
  for idx in range(1, len(G_list)):
    cur_graph = G_list[idx-1]
    next_graph = G_list[idx]
    diff = 0.0
    # only include check-ins for existing nodes
    for node in cur_graph.Nodes():
      nid = node.GetId()
      diff += next_graph.GetIntAttrDatN(nid, 'ckn') - cur_graph.GetIntAttrDatN(nid, 'ckn')
    res.append(diff)
  return res

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
      # month_coeff = float(idx)
      month_coeff = 1
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

def adjust_by_learning(pred_ckn, learning_dict):
  for nid in pred_ckn:
    if learning_dict[nid] > 0:
      pred_ckn[nid] *= learning_dict[nid]

if __name__ == '__main__':
  # load 13 monthly graphs from files
  monthly_graphs = get_monthly_venue_graphs() 
  # generate_monthly_trans_graphs()
  monthly_graphs_trans = get_monthly_trans_graphs()
  print "===== finished loading graphs ====="
  print "\n"

  # get some high-level data about each month
  node_inc_list = get_node_increase_list(monthly_graphs)
  # ckn_total_inc_list = get_ckn_total_increase_list(monthly_graphs)
  ckn_total_inc_list = get_ckn_total_increase_list_cur(monthly_graphs)
  # plt.plot(range(0, len(node_inc_list)), node_inc_list)  
  # show_plot("month", "node increase")
  # plt.plot(range(0, len(ckn_total_inc_list)), ckn_total_inc_list)
  # show_plot("month", "check-in increase")
 
  predict_indices = range(0, 12) # almost range(0, 12)
 
  learn_dict = None

  for idx in predict_indices:
    # cur_graph = monthly_graphs[idx]
    cur_graph = monthly_graphs_trans[idx]
    next_graph = monthly_graphs[idx+1]

    print "===== predict %d-th month" % (idx+1)
    
    pred_ckn = predict_naive(cur_graph, ckn_total_inc_list[idx])
    # pred_ckn = predict_pagerank_naive(cur_graph, ckn_total_inc_list[idx])
    
    # Note: not really a good solution, as we still have to guess the number for new nodes
    # new_node_list = get_node_list(next_graph)
    # pred_ckn = predict_pagerank_new_nodes(cur_graph, new_node_list, ckn_total_inc_list[idx])

    # prev_graph = monthly_graphs[idx-1] if idx > 0 else None
    # dist = get_node_dist(cur_graph, prev_graph)
    # pred_ckn = predict_pagerank_with_dist(cur_graph, ckn_total_inc_list[idx], dist) 
    # pred_ckn = predict_pagerank_with_dist_learn(cur_graph, ckn_total_inc_list[idx], dist, learn_dict) 

    # Note: not working so well as it corrected the mistake too much to the opposite side
    # if learn_dict != None:
    #   adjust_by_learning(pred_ckn, learning_dict)
    
    gold_graph = monthly_graphs[idx+1]
    learn_dict = compare_ckn(cur_graph, gold_graph, pred_ckn, idx)

