from datasource import CsvFileSource
from logplayer import *
from analysis import *
import matplotlib.pyplot as plt

def collect_bins(X,Y):
	zipped = zip(X,Y)
	bins = {}
	for pair in zipped:
		x = pair[0]
		y = pair[1]
		bins.setdefault(x, []).append(y)
	return bins

def aggregate(X,Y):
	bins = collect_bins(X,Y)
	minimums = []
	averages = []
	maximums = []
	sorted_keys = sorted(bins)
	for key in sorted_keys:
		minimums.append( min(bins[key]) )
		averages.append( float(reduce(lambda x,y: x+y, bins[key])) / len(bins[key]) )
		maximums.append( max(bins[key]) )
	return (sorted_keys, minimums, averages, maximums)

def make_plot(ds, title, color):
	player = LogPlayer(ds)
	analyzer = XYAnalyzer(mapper=lambda e: (e.timestamp.tm_hour + (e.timestamp.tm_min/15*15)/60.0, e.proc_ms))
	player.add_analyzer(analyzer)
	player.forward()
	X,Y = analyzer.get_xy()
	X, Ymin, Yavg, Ymax = aggregate(X,Y)

	#plt.axis([0, len(X), 0, max(Yavg)])
	plt.title(title)
	plt.xlabel('Hour of day')
	plt.ylabel('Average processing time (ms)')
	plt.plot(X, Yavg, color)
	plt.show()
	
make_plot( CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv'), 'Average processing times for 24-hour period. Service: skaermkort', 'g' )
make_plot( CsvFileSource('../../../data/log2_2011_q4_rand_mat.csv'), 'Average processing times for 24-hour period. Service: mat', 'b' )
