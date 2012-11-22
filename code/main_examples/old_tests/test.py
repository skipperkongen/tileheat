from datasource import CsvFileSource
from analysis import *
from plotting import *

ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv')

#for e in ds.events():
#	print e

player = LogPlayer(ds)
player.add_analyzer(AverageProc())
player.add_analyzer(AveragePixels())
player.add_analyzer(AverageSize())
player.add_analyzer(AverageProcPerTile())

player.forward()

for analyzer in player.analyzers:
	analyzer.print_report()