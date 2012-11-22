from tileheat import CsvFileSource
from tileheat import LogPlayer
from tileheat.analysis import *
import matplotlib.pyplot as plt

wms_1= CsvFileSource('../../../data/wms_wmts_twoday/wms_day1.csv', event_type='WMS') # 600K events
wmts_1 = CsvFileSource('../../../data/wms_wmts_twoday/wmts_day1.csv', event_type='WMTS') # 600K events
#ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv', event_type='WMS')

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

def get_data(ds):
	player = LogPlayer(ds)
	#analyzer = XYAnalyzer(mapper=lambda e: (e.timestamp.tm_hour + (e.timestamp.tm_min/15*15)/60.0, e.proc_ms ))
	analyzer = XYAnalyzer(mapper=lambda e: (e.timestamp.tm_hour + (e.timestamp.tm_min/15*15)/60.0, 256.0**2 * e.proc_ms / float(e.query.width*e.query.height) ))
	player.add_analyzer(analyzer)
	player.forward()
	X,Y = analyzer.get_xy()
	return aggregate(X,Y)

X1, _, Y1, _ = get_data (wms_1)
X2, _, Y2, _ = get_data (wmts_1)
#X3, _, Y3, _ = get_data(ds)



print 'MAKE FIG'
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.set_title('Average WMS and WMTS tile processing time for 24-hour period')
#ax.set_xlabel('Hour of day')
#ax.set_ylabel('Processing time (ms)')
#ax.set_xlim([0, 250000])
#ax.set_ylim([0,1.2])
ax.plot(X1, Y1, 'k', X2, Y2, 'k:')
ax.legend(('WMS', 'WMTS'), 'upper right', shadow=True)
#ax.plot(X3, Y3, 'b')
#ax.legend(('WMTS'), 'upper right', shadow=True)
# change this to show...
plt.show()
