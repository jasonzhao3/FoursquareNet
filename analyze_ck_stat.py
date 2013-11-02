
import snap
import os, pickle
import numpy as np
import Helper.GraphHelper as GH
import pylab as plt

''' Import Graph: graph is stored in binary form to save space, available in dropbox folder
    sf_trsn_graph_small: A small test graph with only a few venues in sf -- you can use this to test your script first
    sf_trsn_graph: up-to-date venue graph of sf
'''
data_path = '../DataSet/'
result_path = '../DataSet/Analysis/'
#trsn_in = open(os.path.join(data_path, 'sf_trsn'))
time_in = open(os.path.join(data_path, 'sf_time'))

#trsn_list = pickle.load(trsn_in)
time_list = pickle.load(time_in)
ts_list = [item[0] for item in time_list]
ts_list.extend([item[1] for item in time_list])
print min(ts_list), max(ts_list)


