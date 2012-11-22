from tileheat import *
from tileheat.util import *
from tileheat.analysis import *

#ds = CsvFileSource('../../../data/log2_2011_q4_rand_mat.csv') # 90000 events
#ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
ds = CsvFileSource('../../../data/fast2.csv') # 10000 events

def make_heatmap(data):
	"""docstring for make_heatmap"""
	tiling_scheme = TilingScheme.by_name('kms')

	player = LogPlayer( data )
	heatmap = HeatmapAnalyzer( tiling_scheme )
	player.add_analyzer( heatmap )
	player.forward()
	RasterUtil.write_geotiff( heatmap.levels[3.2].matrix, heatmap.tiling_scheme, 3.2, normalize=True, path='heat_d-before.tiff' )
	heatmap.dissipate(0.1, 0.1)
	RasterUtil.write_geotiff( heatmap.levels[3.2].matrix, heatmap.tiling_scheme, 3.2, normalize=True, path='heat_d-after.tiff' )
	
	return player.errors_last_run

print 'Errors:', make_heatmap(ds)

