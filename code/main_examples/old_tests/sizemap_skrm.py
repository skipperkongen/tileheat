from tileheat import *
from tileheat.util import *
from tileheat.analysis import *

#ds = CsvFileSource('../../../data/log2_2011_q4_rand_mat.csv') # 90000 events
ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
#ds = CsvFileSource('../../../data/tmp.csv') # 1000 events
#ds = CsvFileSource('../../../data/tmp2.csv') # 1 events

tiling_scheme = TilingScheme.by_name('kms_mod')

player = LogPlayer(ds)
popmap = HeatmapAnalyzer(tiling_scheme)
# size per 256x256 tile
size_func = lambda event: (256 * 256 * event.answer_size) / float(event.query.width * event.query.height)
costmap = HeatmapAnalyzer(tiling_scheme, valuefunc= size_func )
player.add_analyzer( popmap )
player.add_analyzer( costmap )
player.forward()

for resolution in tiling_scheme.resolutions:
	print 'Writing costmap for: %.2f' % resolution
	matrix_pop = popmap.get_level(resolution).matrix
	matrix_cost = costmap.get_level(resolution).matrix
	print 'DEBUG: max_pop=%d max_cost=%d' % (np.max(matrix_pop), np.max(matrix_cost))
	
	print 'Averaging sizes for: %.2f' % resolution
	for i in range(tiling_scheme.dim_y(resolution)):
		for j in range(tiling_scheme.dim_x(resolution)):
			if matrix_pop[i][j] != 0:
				matrix_cost[i][j] /= float(matrix_pop[i][j])
	
	#matrix_cost = matrix_cost / matrix_pop # average cost per hit
	matrix_cost = MatrixUtil.normalize_matrix(matrix_cost)
	
	RasterUtil.write_geotiff( matrix_cost, tiling_scheme, resolution, path='bytesize-skrm-%s.tiff' % resolution)
