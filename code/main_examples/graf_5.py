from tileheat import CsvFileSource
from tileheat import LogPlayer
from tileheat.analysis import *
import matplotlib.pyplot as plt

#wms_1= CsvFileSource('../../../data/wms_wmts_twoday/wms_day1.csv', event_type='WMS') # 600K events
#wmts_1 = CsvFileSource('../../../data/wms_wmts_twoday/wmts_day1.csv', event_type='WMTS') # 600K events
wms_1 = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv', event_type='WMS')

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
	sums = []
	sorted_keys = sorted(bins)
	for key in sorted_keys:
		sums.append( sum(bins[key]) )
	return (sorted_keys, sums)

def get_data(ds):
	player = LogPlayer(ds)
	analyzer = XYAnalyzer(mapper=lambda e: (e.timestamp.tm_hour + (e.timestamp.tm_min/30*30)/60.0, 1/30.0 ))
	player.add_analyzer(analyzer)
	player.forward()
	X,Y = analyzer.get_xy()
	return aggregate(X,Y)

X1, Y1 = get_data (wms_1)
#X2, _, Y2, _ = get_data (wmts_1)
#X3, _, Y3, _ = get_data(ds)



print 'MAKE FIG'
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Average WMS load for Q4 of 2011')
#ax.set_xlabel('Hour of day')
#ax.set_ylabel('Requests per minute')
ax.plot(X1, Y1, 'k')
# change this to show...
plt.show()
