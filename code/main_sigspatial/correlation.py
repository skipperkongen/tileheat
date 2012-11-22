from tileheat import CsvFileSource
from tileheat import LogPlayer
from tileheat.analysis import *
import matplotlib
import matplotlib.pyplot as plt

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

load_mapper = lambda e: (e.timestamp.tm_hour + (e.timestamp.tm_min/30*30)/60.0, 1/30.0 )
latency_mapper = lambda e: (e.timestamp.tm_hour + (e.timestamp.tm_min/30*30)/60.0, e.proc_ms )

X1, Y1 = get_data(path, load_mapper, sum_for_bin)
Y1 = normalize(Y1)
X2, Y2 = get_data(path, latency_mapper, average_for_bin)

#ar = (1, 1)
#ar = (8, 5)
ar = (1.61803399, 1)
factor_x = 6
factor_y = 3

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)

#fig = plt.figure(figsize=(ar[0]*factor_x, ar[1]*factor_y))
fig = plt.figure()
print fig.get_dpi()
ax1 = fig.add_subplot(111)                     
ax1.plot(X1, Y1, 'b', linewidth=2)
ax1.set_xlabel('Hour of day')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Load (normalized)', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')
ax1.axis((0,24,0,1.2))

ax2 = ax1.twinx()
ax2.plot(X2, Y2, 'g', linewidth=2)
ax2.set_ylabel('Latency (ms)', color='g')
for tl in ax2.get_yticklabels():
    tl.set_color('g')
ax2.axis((0,24,0,1.2*max(Y2)))
plt.savefig("correlation.png")
        
