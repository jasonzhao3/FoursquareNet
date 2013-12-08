import snap
from Queue import Queue
from collections import Counter
import pylab as plt
import numpy as np
import Helper.GraphHelper as GH
import Helper.TimeHelper as TH
import Helper.VenueHelper as VH
import pickle, os

def make_key(v, w):
    if v < w:
        return (v,w)
    else:
        return (w,v)

def get_edge_weight(graph):
    edge_weight = Counter()  
    for edge in graph.Edges():
        src_nid = edge.GetSrcNId()
        dst_nid = edge.GetDstNId()
        edge_id = graph.GetEId(src_nid, dst_nid)
        edge_weight[(src_nid, dst_nid)] += graph.GetIntAttrDatE(edge_id, 'trsn_cnt')
    print edge_weight, len(edge_weight)
    return edge_weight

# node weight used for modularity calculation
def get_node_weight(graph):
    node_weight = Counter()
    for node in graph.Nodes():
        nid = node.GetId()
        node_weight[nid] += graph.GetIntAttrDatN(nid, 'ckn')
    print node_weight, len(node_weight)
    return node_weight

# recursion: has both return value and reference updates
def recur_dependency(deltas, sigmas, children, v, w, edge_weight):
    weight = edge_weight[(v,w)] + edge_weight[(w, v)]
    gamma = 1.0 / np.sqrt(weight)
    # leaf node
    if not children[w]:
        key = make_key(v,w)
        deltas[key] = float(sigmas[v]) / sigmas[w] * gamma
        return deltas[key]
    # normal recursion
    tmp_delta = 1.0
    for kid in children[w]:
        tmp_delta += recur_dependency(deltas, sigmas, children, w, kid, edge_weight)
    key = make_key(v,w)
    deltas[key] = float(sigmas[v]) / sigmas[w] * tmp_delta * gamma
    return deltas[key]

def get_dependency(sigmas, children, root_id, edge_weight):
    deltas = {}
    for kid in children[root_id]:
        recur_dependency(deltas, sigmas, children, root_id, kid, edge_weight)
    return deltas

def bfs(graph, root_id, path_lens, sigmas, children):
    path_lens[root_id] = 0
    sigmas[root_id] = 1
    children[root_id] = []
    
    q = Queue()
    q.put(root_id)
    while q.qsize() > 0:
        curr_nid = q.get()
        curr_node = graph.GetNI(curr_nid)
        for i in xrange(curr_node.GetOutDeg()):
            dst_nid = curr_node.GetOutNId(i)
            # new node - new shortest path, only new node need enqueue
            if dst_nid not in path_lens:
                path_lens[dst_nid] = path_lens[curr_nid] + 1
                sigmas[dst_nid] = sigmas[curr_nid]
                children[dst_nid] = []
                children[curr_nid].append(dst_nid)
                q.put(dst_nid)
            # another shortest path
            elif path_lens[dst_nid] == path_lens[curr_nid] + 1:
                sigmas[dst_nid] += sigmas[curr_nid]
                children[curr_nid].append(dst_nid)
            # otherwise -may be parent, or non-shortest-path node, do nothin
 
def update_ap_dependency(s_dep, ap_btwness, kcnt, cn):
    for edge, val in s_dep.iteritems():
        if ap_btwness[edge] <= cn:
            ap_btwness[edge] += val
            kcnt[edge] += 1

def update_est_btwness(ap_btwness, kcnt, n):
    for edge, val in ap_btwness.iteritems():
        k = kcnt[edge]
        ap_btwness[edge] = ap_btwness[edge] * float(n) / k

def get_ap_btwness(graph, sample_limit, cn, n, edge_weight):
    ap_btwness = Counter()
    kcnt = Counter()
    node_set = set()
    cnt = 0
    while cnt <= sample_limit:
        nid = graph.GetRndNId()
        path_lens = {}
        sigmas = {}
        children = {}
        if nid not in node_set:
            cnt += 1
            node_set.add(nid)
            bfs(graph, nid, path_lens, sigmas, children)
            s_dep = get_dependency(sigmas, children, nid, edge_weight)
            update_ap_dependency(s_dep, ap_btwness, kcnt, cn)
        print 'finish one more pass, now ', cnt
    update_est_btwness(ap_btwness, kcnt, n)
    return ap_btwness

def get_edge_to_remove(graph, edge_weight):
    # algorithm 2
    sample_limit = n / 500
    cn = 3 * n
    ap_btwness = get_ap_btwness(graph, sample_limit, cn, n, edge_weight)
    edge_list = ap_btwness.keys()
    ap_btwness_list = ap_btwness.values()
    comb_list = zip(edge_list, ap_btwness_list)
    comb_list.sort(key=lambda t:t[1], reverse=True)
    # return edge with largest btwness
    return comb_list[0][0]

def get_m(node_weight):
    return float(sum(node_weight.values()))

def get_s(n, communities):
    s = [-1]*n
    label = 0
    for cmty in communities:
        for nid in cmty:
            s[nid] = label
        label += 1
    return s

def get_B(graph, node_weight, m):
    B = []
    # node iteration is ordered
    for ni in graph.Nodes():
        row = []
        ni_id = ni.GetId()
        for nj in graph.Nodes():
            nj_id = nj.GetId()
            si = node_weight[ni_id]
            sj = node_weight[nj_id]
            if graph.IsEdge(ni_id, nj_id):
               row.append(1.0 - si * sj / (2*m))
            else:
                row.append(0.0 - si *sj / (2*m))
        B.append(row)
        print "append one more row into B!"
    return B

def save_list(label_list, data_path, filename):
    out_file = os.path.join(data_path, filename)
    out_file = open(out_file, 'wb')
    pickle.dump(label_list, out_file)
    out_file.close()            
    
def get_modularity(communities, n, m, B):
    s = get_s(n, communities)
    return 1.0 / (4*m) * np.dot(s, np.dot(s, B)), s

# file configuration
# TODO: create a configuration module
graph_path = '../DataSet/GraphData/'
venue_path = '../DataSet/VenueData/'
community_path = '../DataSet/Community/'
result_path = '../DataSet/Analysis/'
graph_name = 'sf_venue_small'
category_name = 'category_map.json'
pcategory_name = 'pcategory_map.json'


# load graph and corresponding category_list
'''
    Currently, the graph has node attribute:
    - vid
    - ckn (insofar, checkin number)
    - sts (start timestamp)
    - ets (end timestamp)
    - lat
    - lng
    - category
    - pcategor
    
    And edge attribute:
    - trsn_cnt
    - duration
'''
g = GH.load_graph(graph_path, graph_name)
n = g.GetNodes()
print g.GetNodes(), g.GetEdges()

edge_weight = get_edge_weight(g)
node_weight = get_node_weight(g)

undirected_g = GH.convert_undirected_graph(g)
m = get_m(node_weight)
B = get_B(undirected_g, node_weight, m)
save_list(B, community_path, 'B_matrix')

num_community = 0

mod_list = []
while num_community < 10:
    edge = get_edge_to_remove(undirected_g, edge_weight)
    undirected_g.DelEdge(edge[0], edge[1])
    communities = snap.TCnComV()
    snap.GetWccs(undirected_g, communities)
    if num_community != communities.Len():
        num_community = communities.Len()
        modularity, s = get_modularity(communities, n, m, B)
        save_list(s, community_path, 'community_' + str(num_community))
        print modularity
        mod_list.append(modularity)
    print num_community
print mod_list
    
