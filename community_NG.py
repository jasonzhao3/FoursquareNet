import snap
from Queue import Queue
from collections import Counter
import pylab as plt
import numpy as np
import Helper.GraphHelper as GH
import Helper.TimeHelper as TH
import Helper.VenueHelper as VH

def make_key(v, w):
    if v < w:
        return (v,w)
    else:
        return (w,v)

def get_weight_dict(graph):
    weight_dict = Counter()  
    for edge in graph.Edges():
        src_nid = edge.GetSrcNId()
        dst_nid = edge.GetDstNId()
        edge_id = graph.GetEId(src_nid, dst_nid)
        weight_dict[(src_nid, dst_nid)] += graph.GetIntAttrDatE(edge_id, 'trsn_cnt')
    print weight_dict, len(weight_dict)
    return weight_dict
 
# recursion: has both return value and reference updates
def recur_dependency(deltas, sigmas, children, v, w, weight_dict):
    weight = weight_dict[(v,w)] + weight_dict[(w, v)]
    gamma = 1.0 / np.sqrt(weight)
    # leaf node
    if not children[w]:
        key = make_key(v,w)
        deltas[key] = float(sigmas[v]) / sigmas[w] * gamma
        return deltas[key]
    # normal recursion
    tmp_delta = 1.0
    for kid in children[w]:
        tmp_delta += recur_dependency(deltas, sigmas, children, w, kid, weight_dict)
    key = make_key(v,w)
    deltas[key] = float(sigmas[v]) / sigmas[w] * tmp_delta * gamma
    return deltas[key]

def get_dependency(sigmas, children, root_id, weight_dict):
    deltas = {}
    for kid in children[root_id]:
        recur_dependency(deltas, sigmas, children, root_id, kid, weight_dict)
    return deltas

def update_dependency(s_dep, dependency):
    for edge, val in s_dep.iteritems():
        dependency[edge] += val

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
 

def get_btwness(graph, root_id, btwness, weight_dict):
    # path_lens: a dictionary to keep record of shortest path length to each node
    # sigmas: a dictionary to keep record of sigmas
    # children: a dictionary to keep all children of a node
    path_lens = {}
    sigmas = {}
    children = {}
    # longest path length => not necessarily a leaf node, instead no children means leaf-node 
    bfs(graph, root_id, path_lens, sigmas, children)
    s_dep = get_dependency(sigmas, children, root_id, weight_dict)
    update_dependency(s_dep, btwness)

def update_ap_dependency(s_dep, ap_btwness, kcnt, cn):
    for edge, val in s_dep.iteritems():
        if ap_btwness[edge] <= cn:
            ap_btwness[edge] += val
            kcnt[edge] += 1

def update_est_btwness(ap_btwness, kcnt, n):
    for edge, val in ap_btwness.iteritems():
        k = kcnt[edge]
        ap_btwness[edge] = ap_btwness[edge] * float(n) / k

def get_ap_btwness(graph, sample_limit, cn, n, weight_dict):
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
            s_dep = get_dependency(sigmas, children, nid, weight_dict)
            update_ap_dependency(s_dep, ap_btwness, kcnt, cn)
        print 'finish one more pass, now ', cnt
    update_est_btwness(ap_btwness, kcnt, n)
    return ap_btwness

       
 

# file configuration
# TODO: create a configuration module
graph_path = '../DataSet/GraphData/'
venue_path = '../DataSet/VenueData/'
result_path = '../DataSet/Analysis/'
graph_name = 'sf_venue_graph'
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

undirected_g = GH.convert_undirected_graph(g)
weight_dict = get_weight_dict(g)
'''
# algorithm 1
btwness = Counter()
for node in undirected_g.Nodes():
    get_btwness(undirected_g, node.GetId(), btwness, weight_dict)

btwness_list = btwness.values()
btwness_list.sort(reverse=True)
print btwness_list
print g.GetEdges(), len(btwness_list)
''' 

# algorithm 2
sample_limit = n / 20
cn = 3 * n
ap_btwness = get_ap_btwness(undirected_g, sample_limit, cn, n, weight_dict)
ap_btwness_list = ap_btwness.values()
ap_btwness_list.sort(reverse=True)

plt.figure()
plt.semilogy(btwness_list, '--', color='red', label='algorithm1')
plt.semilogy(ap_btwness_list, '-', color='blue', label='algorithm2')
plt.legend(loc='upper left')
plt.xlabel('x')
plt.ylabel('betweeness centrality')
plt.savefig('Q2.png')


    

