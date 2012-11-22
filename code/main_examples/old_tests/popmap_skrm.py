from tileheat import *
from tileheat.util import *
from tileheat.analysis import *

#ds = CsvFileSource('../../../data/log2_2011_q4_rand_mat.csv') # 90000 events
ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
#ds = CsvFileSource('../../../data/tmp.csv') # 1000 events
#ds = CsvFileSource('../../../data/tmp2.csv') # 1 events

tiling_scheme = TilingScheme.by_name('kms_mod')

player = LogPlayer(ds)
heatmap = HeatmapAnalyzer(tiling_scheme)
player.add_analyzer( heatmap )
player.forward()

RasterUtil.write_geotiff_heatmap( heatmap, normalize=True, path_prefix='pop-skrm')

print 'Errors: %d' % player.errors_last_run
