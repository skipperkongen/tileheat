from tileheat import CsvFileSource
from tileheat import LogPlayer
from tileheat.analysis import *
import matplotlib
import matplotlib.pyplot as plt
from time import mktime
from datetime import datetime          

path = '../../../data/log2_2011_q4_rand_skrm.csv'
#path = '../../../data/fast.csv'

def collect_bins(X,Y):
	zipped = zip(X,Y)
	bins = {}
	for pair in zipped:
		x = pair[0]
		y = pair[1]
		bins.setdefault(x, []).append(y)
	return bins

def sum_for_bin(X,Y):
	bins = collect_bins(X,Y)
	sums = []
	sorted_keys = sorted(bins)
	for key in sorted_keys:
		sums.append( sum(bins[key]) )
	return (sorted_keys, sums)

def average_for_bin(X,Y):
	bins = collect_bins(X,Y) 
	averages = []
	sorted_keys = sorted(bins)
	for key in sorted_keys:
		bin = bins[key]
		averages.append( sum(bin) / float(len(bin)) )
	return (sorted_keys, averages)

def get_data(path, mapper, reducer):
	ds = CsvFileSource(path, event_type='WMS')
	player = LogPlayer(ds)
	analyzer = XYAnalyzer(mapper=mapper)
	player.add_analyzer(analyzer)
	player.forward()
	X,Y = analyzer.get_xy()
	#print X,Y
	return reducer(X,Y)
                                        
def normalize(seq):
	mv = max(seq)
	return map(lambda x: x/float(mv), seq)
 

#mapper = lambda e: (e.timestamp.tm_yday + (e.timestamp.tm_hour/12.0), 1 )
mapper = lambda e: (datetime.fromtimestamp(mktime(e.timestamp)).isocalendar()[1]  +  (e.timestamp.tm_wday / 7.0) + (e.timestamp.tm_hour)/(24*7.0), 1 )                                                                         

X1, Y1 = get_data(path, mapper, sum_for_bin)
Y1 = normalize(Y1)

avg_load = sum(Y1) / float(len(Y1))
Y2 = [avg_load]*len(X1)

X2 = X1

ar = (1.61803399, 1)
factor_x = 4
factor_y = 2
dpi=320

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)

fig = plt.figure()
#fig = plt.figure(figsize=(ar[0]*factor_x, ar[1]*factor_y), dpi=dpi)
ax1 = fig.add_subplot(111)                     
ax1.plot(X1, Y1, 'b', X2, Y2, 'r', linewidth=2)
ax1.set_xlabel('Week')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Load (normalized)', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('k')
ax1.axis((46,51,0,1.1))
plt.savefig("anomaly.png")
        
