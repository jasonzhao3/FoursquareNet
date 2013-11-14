import numpy as np
from numpy import arange, array, ones, linalg


def gen_degree_hist( graph ):
	deg_cnt_v = snap.TIntPrV()
	snap.GetDegCnt( graph, deg_cnt_v )
	return deg_cnt_v


def get_mle_alpha(point_list, x_min):
    point_list = filter(lambda x:x >= x_min, point_list)
    ratio_list = np.log(np.divide(point_list, x_min))
    est_alpha = 1 + num_points / np.sum(ratio_list)
    return est_alpha

def gen_powerlaw_p(x, alpha, x_min):
    return (alpha-1)/x_min * pow((x/x_min), -alpha)

def get_powerlaw_y(point_list, alpha, x_min):
    return [gen_powerlaw_p(x, alpha, x_min) for x in point_list]



