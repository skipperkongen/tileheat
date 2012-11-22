from tileheat import *
from tileheat.util import *
from tileheat.analysis import *
import matplotlib.pyplot as plt

#ds = CsvFileSource('../../../data/log2_2011_q4_rand_mat.csv') # 90000 events
ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv') # 90000 events
#ds = CsvFileSource('../../../data/tmp.csv') # 1000 events
#ds = CsvFileSource('../../../data/tmp2.csv') # 1 events

tiling_scheme = TilingScheme.by_name('kms_mod')

player = LogPlayer(ds)
heatmap = HeatmapAnalyzer(tiling_scheme)
player.add_analyzer( heatmap )
player.forward()

resolutions = [res for res in sorted(heatmap.levels, reverse=True) ]

total_cells = 0	

for resolution in resolutions:
	level = heatmap.get_level( resolution )

	print 'Stats for level:', resolution
	print '---'
	print 'Total heat:', level.total_heat()
	print 'Total cells:', level.num_cells()
	print 'Cells w. heat', level.num_cells_affected()

	acc = MatrixUtil.accumulate_inorder( onesum, onesum=True )
	
	# plot values
	plt.title('Tile cache efficiency for resolution %.2f' % resolution)
	plt.xlabel('Number of tiles cached')
	plt.ylabel('Cache hits')
	X = range(1,len(acc)+1)
	plt.axis([0, len(acc)+1, 0, 1.2])	
	plt.plot(X, acc, 'b-')
	print 'Saving plot for %.2f' % resolution
	plt.savefig("acc_%.2f.png" % resolution)
	plt.clf()
