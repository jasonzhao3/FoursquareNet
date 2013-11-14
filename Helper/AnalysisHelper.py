import snap
import numpy as np
from numpy import arange, array, ones, linalg


def gen_degree_hist( graph ):
	deg_cnt_v = snap.TIntPrV()
	snap.GetDegCnt( graph, deg_cnt_v )
	return deg_cnt_v

def hist_to_pt_list(deg_v, deg_cnt):
    point_list = []
    for idx, deg in enumerate(deg_v):
        tmp_list = [deg]*deg_cnt[idx]
        point_list.extend(tmp_list)
    return point_list

def get_mle_alpha(point_list, x_min):
    point_list = filter(lambda x:x >= x_min, point_list)
    ratio_list = np.log(np.divide(point_list, x_min))
    est_alpha = 1 + len(point_list) / np.sum(ratio_list)
    return est_alpha

def gen_powerlaw_p(x, alpha, x_min):
    return (alpha-1.0)/x_min * pow((x/x_min), -alpha)

def get_powerlaw_y(point_list, alpha, x_min, scale):
    return [gen_powerlaw_p(x, alpha, x_min)*scale for x in xrange(x_min, len(point_list))]



