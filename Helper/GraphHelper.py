import snap
import random

	
def gen_degree_hist( graph ):
	deg_cnt_v = snap.TIntPrV()
	snap.GetDegCnt( graph, deg_cnt_v )
	return deg_cnt_v
