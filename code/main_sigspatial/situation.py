from tileheat import CsvFileSource
from tileheat import LogPlayer
from tileheat.analysis import *
import matplotlib.pyplot as plt
from time import mktime
from datetime import datetime          

#path = '../../../data/log2_2011_q4_rand_skrm.csv'
path = '../../../data/fast.csv'

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

def get_data(path, mpr, aggregator):
	ds = CsvFileSource(path, event_type='WMS')
	player = LogPlayer(ds)
	analyzer = XYAnalyzer(mapper=mpr)
	player.add_analyzer(analyzer)
	player.forward()
	X,Y = analyzer.get_xy()
	return aggregator(X,Y)
                                        
def normalize(seq):
	mv = max(seq)
	return map(lambda x: x/float(mv), seq)

load_mapper = lambda e: (e.timestamp.tm_yday + (e.timestamp.tm_hour/4.0, 1 )

X1, Y1 = get_data(path, load_mapper, sum_for_bin)
Y1 = normalize(Y1)

avg_load = sum(Y1) / float(len(Y))
Y2 = [avg_load]*len(X)

X2 = X1

ar = (1.61803399, 1)
factor = 2.5
fig = plt.figure(figsize=(ar[0]*factor, ar[1]*factor))
ax1 = fig.add_subplot(111)                     
ax1.plot(X1, Y1, 'b', X2, Y2, 'r')
#ax1.set_xlabel('Hour of day')
# Make the y-axis label and tick labels match the line color.
#ax1.set_ylabel('Average load (normalized)', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('k')
ax1.axis((0,24,0,1.2*max(Y1)))
plt.savefig("anomaly.png")
        
