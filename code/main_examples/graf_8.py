from tileheat import *
from tileheat.util import *
from tileheat.analysis import *

#ds = CsvFileSource('../../../data/log2_2011_q4_rand_mat.csv') # 90000 events
#ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
#ds1 = CsvFileSource('../../../data/wms_wmts_twoday/wms_day1.csv')
#ds2 = CsvFileSource('../../../data/wms_wmts_twoday/wms_day2.csv')
ds1 = CsvFileSource('../../../data/prefix_log2_2011_q4_rand_skrm.csv')
ds2 = CsvFileSource('../../../data/postfix_log2_2011_q4_rand_skrm.csv')
#ds = CsvFileSource('../../../data/tmp.csv') # 1000 events
#ds = CsvFileSource('../../../data/tmp2.csv') # 1 events

def make_heatmap(data, path):
	"""docstring for make_heatmap"""
	tiling_scheme = TilingScheme.by_name('kms_mod')

	player = LogPlayer( data )
	heatmap = HeatmapAnalyzer( tiling_scheme )
	player.add_analyzer( heatmap )
	player.forward()
	RasterUtil.write_geotiff( heatmap.levels[3.2].matrix, heatmap.tiling_scheme, 3.2, normalize=True, path=path )
	
	return player.errors_last_run

print 'Errors:', make_heatmap(ds1, 'heat-pre')
print 'Errors:', make_heatmap(ds2, 'heat-post')

