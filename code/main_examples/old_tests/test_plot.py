from datasource import CsvFileSource
from logplayer import *
from analysis import *
from pylab import *
from matplotlib import pyplot

ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv')

#for e in ds.events():
#	print e

player = LogPlayer(ds)
#player.add_analyzer(AverageProc())
#player.add_analyzer(AveragePixels())
#player.add_analyzer(AverageSize())
#player.add_analyzer(AverageProcPerTile())

# , 
pix_bytes = XYAnalyzer(
	mapper=lambda e: (e.answer_size, e.proc_ms), 
	filter=lambda e: e.bbox_query.format == 'IMAGE/PNG')
#	filter=lambda e: e.format == 'IMAGE/JPEG')


player.add_analyzer(pix_bytes)
player.forward()

X,Y = pix_bytes.get_xy()
#pyplot.xscale('log')
#pyplot.yscale('log')
xlabel('Resolution (meter per pixel)')
ylabel('Processing time (ms)')
axis([0, max(X)/2, 0, max(Y)/32])
#title('Pixels to bytesize ratio for WMS GetMap JPEG requests')
title('Resoutions to processing time ratio for WMS GetMap PNG requests')
scatter(X,Y, s=0.1, marker='o', c='r')
show()


#for analyzer in player.analyzers:
#	analyzer.print_report()