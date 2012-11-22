from tileheat import *
from tileheat.util import *
from tileheat.analysis import *

#ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
#ds = CsvFileSource('../../../data/fast.csv') # 90000 events
ds1 = CsvFileSource('../../../data/tileheat_dump/e_1.csv')
ds2 = CsvFileSource('../../../data/tileheat_dump/e_2.csv')
ds3 = CsvFileSource('../../../data/tileheat_dump/e_3.csv')
ds4 = CsvFileSource('../../../data/tileheat_dump/e_4.csv')

data = [ds1, ds2, ds3, ds4]

def make_heatmap(data, path):
	"""docstring for make_heatmap"""
	tiling_scheme = TilingScheme.by_name('kms')
	print "Analyzing data"
	player = LogPlayer( data )
	heatmap = HeatmapAnalyzer( tiling_scheme )
	player.add_analyzer( heatmap )
	player.forward()
	print 'write heatmap'
	RasterUtil.write_geotiff( heatmap.levels[3.2].matrix, heatmap.tiling_scheme, 3.2, normalize=True, path=path )	
	return player.errors_last_run

for i in range(len(data)):
	make_heatmap(data[i], 'heatmap-e_%d.tiff' % (i+1))
