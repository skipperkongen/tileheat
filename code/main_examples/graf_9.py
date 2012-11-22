from tileheat import *
from tileheat.util import *
from tileheat.analysis import *

#ds = CsvFileSource('../../../data/log2_2011_q4_rand_mat.csv') # 90000 events
ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
#ds1 = CsvFileSource('../../../data/wms_wmts_twoday/wms_day1.csv')
#ds2 = CsvFileSource('../../../data/wms_wmts_twoday/wms_day2.csv')
#ds = CsvFileSource('../../../data/tmp.csv') # 1000 events
#ds = CsvFileSource('../../../data/tmp2.csv') # 1 events

tiling_scheme = TilingScheme.by_name('kms_mod')

player = LogPlayer( ds )
heatmap = HeatmapAnalyzer( tiling_scheme )
player.add_analyzer( heatmap )
player.forward()
# before
RasterUtil.write_geotiff( heatmap.levels[3.2].matrix, heatmap.tiling_scheme, 3.2, normalize=True, path='heat_before_d.tiff' )
heatmap.dissipate(0.05, 0.015)
# after
RasterUtil.write_geotiff( heatmap.levels[3.2].matrix, heatmap.tiling_scheme, 3.2, normalize=True, path='heat_after_d.tiff')
