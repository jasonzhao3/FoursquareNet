'''
    This script is used to combine several small splited transition files into one complete transition file.
    
    Because we first split 1.5GB original transition file into several small files. 
    Then we extract region-related(e.g. SF-related) transition info from each of the file.
    Finally we use this script to combine those results together into a complete file.
'''


import os, pickle
from string import ascii_lowercase as alpha_str

data_path = '../DataSet/Transition/'
trsn_prefix = 'out_trsn_checkin_seg_a'
time_prefix = 'out_time_checkin_seg_a'
trsn_list = []
time_list = []
for c in alpha_str:
    if c == 'c':
        break
    file_name = os.path.join(data_path, trsn_prefix + c)
    infile = open(file_name, 'r')
    trsn_list.extend(pickle.load(infile))
    infile.close()
    
    file_name = os.path.join(data_path, time_prefix + c)
    infile = open(file_name, 'r')
    time_list.extend(pickle.load(infile))
    infile.close()
# small_new only contains checkin in a b two files
out_trsn = os.path.join(data_path, 'sf_trsn_small_new')
out_time = os.path.join(data_path, 'sf_time_small_new')

out_trsn = open(out_trsn, 'wb')
out_time = open(out_time, 'wb')
pickle.dump(trsn_list, out_trsn)
pickle.dump(time_list, out_time)
out_trsn.close()                                                                                                                                                                                      
out_time.close()
print "succesffully combine all data"

