from datasource import CsvFileSource
from logplayer import *
from analysis import *
from pylab import *
from matplotlib import pyplot

ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv')

player = LogPlayer(ds)

analyzer = XYAnalyzer(mapper=lambda e: (e.timestamp.tm_hour, e.proc_ms))

player.add_analyzer(analyzer)
player.forward()
print analyzer.hits

X,Y = analyzer.get_xy()
#pyplot.xscale('log')
#pyplot.yscale('log')
xlabel('Time of day')
ylabel('Processing time (ms)')
axis([0, 24, 0, max(Y)])
title('Processing times, for each hour of the day')
scatter(X,Y, s=0.1, marker='o', c='r')
show()
