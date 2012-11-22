from tileheat import *
from tileheat.util import *
from tileheat.analysis import *
import matplotlib.pyplot as plt


#ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
#ds = CsvFileSource('../../../data/fast.csv') # 90000 events
ds = CsvFileSource('../../../data/tileheat_dump/e_1.csv')

def make_heatmap(data):
	"""docstring for make_heatmap"""
	tiling_scheme = TilingScheme.by_name('kms')
	print "Analyzing data"
	player = LogPlayer( data )
	heatmap = HeatmapAnalyzer( tiling_scheme )
	player.add_analyzer( heatmap )
	player.forward()
	return heatmap

heatmap = make_heatmap(ds)
for resolution in (3.2, 102.4):
	plt.clf()
	Y = cummulative_distribution( heatmap.levels[resolution].matrix )
	print len(Y)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title('Skew for resolution %.2f' % resolution)
	ax.set_xlabel('Tiles cached')
	ax.set_ylabel('Hits')
	ax.set_xlim([0, len(Y)])
	ax.set_ylim([0,1.1])
	ax.plot(Y)
	plt.savefig("skew-%.1f.png" % resolution)
	
