from tileheat import *
from tileheat.util import *
from tileheat.analysis import *    
import sys

#ds = CsvFileSource('../../../data/log2_2011_q4_rand_mat.csv') # 90000 events
ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
#ds1 = CsvFileSource('../../../data/wms_wmts_twoday/wms_day1.csv')
#ds2 = CsvFileSource('../../../data/wms_wmts_twoday/wms_day2.csv')
#ds = CsvFileSource('../../../data/tmp.csv') # 1000 events
#ds = CsvFileSource('../../../data/tmp2.csv') # 1 events

path = '../../../data/tileheat_dump/'
files = ['a_1.csv', 'a_2.csv', 'a_3.csv', 'a_4.csv']

tiling_scheme = TilingScheme.by_name('kms')

heatmap = HeatmapAnalyzer( tiling_scheme )

for file in files:
	abspath = '%s%s' % (path, file)
	print 'Analyzing', abspath
	ds = CsvFileSource( abspath )
	player = LogPlayer( ds )
	player.add_analyzer( heatmap )
	player.forward()

level = heatmap.levels[3.2]

