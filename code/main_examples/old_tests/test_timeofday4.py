from datasource import CsvFileSource
from logplayer import *
from analysis import *
import matplotlib.pyplot as plt

SAMPLE_SIZE = 90000.0
SKRM_SCALE = (0.58 * 2000000.0) / SAMPLE_SIZE
MAT_SCALE = (0.05 * 2000000.0) / SAMPLE_SIZE

def collect_bins(X,Y):
	zipped = zip(X,Y)
	bins = {}
	for pair in zipped:
		x = pair[0]
		y = pair[1]
		bins.setdefault(x, []).append(y)
	return bins

def aggregate(X, Y, correction=1):
	bins = collect_bins(X,Y)
	totals = []
	sorted_keys = sorted(bins)
	for key in sorted_keys:
		totals.append( (reduce(lambda x,y: x+y, bins[key]) / 15.0) * correction )
	return (sorted_keys, totals)

def make_plot(ds, title, color, correction=1):
	player = LogPlayer(ds)
	analyzer = XYAnalyzer(mapper=lambda e: (e.timestamp.tm_hour + (e.timestamp.tm_min/15*15)/60.0, 1))
	player.add_analyzer(analyzer)
	player.forward()
	X,Y = analyzer.get_xy()
	X,Y = aggregate(X,Y, correction)

	#plt.axis([0, len(X), 0, max(Yavg)])
	plt.title(title)
	plt.xlabel('Hour of day')
	plt.ylabel('Requests per minute')
	plt.plot(X, Y, color)
	plt.show()
	
make_plot( CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv'), 'Requests per minute, 24-hour period. Service: skaermkort', 'g', SKRM_SCALE )
make_plot( CsvFileSource('../../../data/log2_2011_q4_rand_mat.csv'), 'Requests per minute, 24-hour period. Service: mat', 'b', MAT_SCALE )
