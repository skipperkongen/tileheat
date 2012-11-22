from tileheat import *
from tileheat.util import *
from tileheat.analysis import *
import matplotlib.pyplot as plt

ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
#ds1 = CsvFileSource('../../../data/wms_wmts_twoday/wms_day1.csv')
#ds2 = CsvFileSource('../../../data/wms_wmts_twoday/wms_day2.csv')
#ds1 = CsvFileSource('../../../data/prefix_log2_2011_q4_rand_skrm.csv')
#ds2 = CsvFileSource('../../../data/postfix_log2_2011_q4_rand_skrm.csv')
#ds = CsvFileSource('../../../data/tmp.csv') # 1000 events
#ds = CsvFileSource('../../../data/tmp2.csv') # 1 events

player = LogPlayer( ds )
ts = TilingScheme.by_name('kms_mod')
resolutions = sorted(ts.resolutions)
print "Resolutions", resolutions
keyfunc = lambda e: resolutions.index(ts.nearest_resolution(e.query.x_res))
analyzer = KeycountAnalyzer(key=keyfunc)
player.add_analyzer( analyzer )
player.forward()

X,Y = analyzer.counter.to_xy()


print 'X', X
print 'Y',Y

print 'MAKE FIG'
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.set_title('Average WMS processing time for Q4 of 2011')
#ax.set_xlabel('Hour of day')
#ax.set_ylabel('Processing time (ms)')
#ax.set_yscale('log')
ax.scatter(X, Y)
# change this to show...
plt.show()
