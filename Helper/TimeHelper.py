import time
from datetime import datetime as dt

def gmt_to_unix(gmt_time):
    return int(time.mktime(dt.strptime(gmt_time, '%Y%m%d%H%M').timetuple())) - 3600*8

# start_time: %Y%m%d%H%M i.e. 201201010000
# end_time: %Y%m%d%H%M  i.e. 201301010000
# duration: unit - day i.e. 30
def gen_ts_list(start_time, end_time, duration):
    start_unix = gmt_to_unix(start_time)
    end_unix = gmt_to_unix(end_time)
    duration_unix = 3600*24*duration
    ts = start_unix
    ts_list = []
    while(ts < end_unix):
       ts_list.append(ts)
       ts += duration_unix
    return ts_list

