from tileheat import *
from tileheat.util import *
from tileheat.analysis import *
from tileheat.optimization import *
import numpy as np
import matplotlib.pyplot as plt
import cPickle

trad = CsvFileSource('../../../data/wms_wmts_twoday/wms_day1.csv') # 600K events
vald = CsvFileSource('../../../data/wms_wmts_twoday/wms_day2.csv') # 600K events
date_series = [
	['10_10','10_07','10_06','10_11'],
	['10_18','10_17','10_14','10_19'],
	['10_26','10_25','10_24','10_27'],
	['11_22','11_21','11_18','11_23'],
	['12_02','12_01','11_30','12_05'],
	['12_23','12_22','12_21','12_26']
]

in_files = map(lambda x: map(lambda y: 'data/%s.csv' % (data_dir,y), x), date_series)

def accumulate(seq):
	for i in range(1, len(seq)):
		seq[i] += seq[i-1]

def get_heatmap(datasources, squish=True):
	heatmap = HeatmapAnalyzer( TilingScheme.by_name('kms_mod') )		
	for ds in datasources:
		player = LogPlayer( ds )			
		player.add_analyzer( heatmap )
		player.forward()
	if squish:
		heatmap.squish()
	return heatmap

def eval_heat(heatmap, opt_heatmap):

	return accumulate( hits )

def dump_to_file(obj, filename):
	cPickle.dump(obj, open(filename, 'wb'))

def read_from_file(filename):
	return cPickle.load(open(filename, 'rb'))

# produce results
for i in range( len( in_files ) ):

	##
	# OPT
	##
	
	vald = CsvFileSource( in_files[-1], 'WMS')
	opt_heatmap = get_heatmap( [vald] )	
	Y_OPT = map( lambda cell: cell.value, opt_heatmap.sorted_cells() )
	accumulate( Y_OPT )
	dump_to_file(Y_OPT, 'data/%s-sens_opt.ys' % date_series[i][-1])

	##
	# HEAT
	##
	for j in range(1, len(in_files[i])):
		
		trad = [CsvFileSorce(file, 'WMS') for file in in_files[i][:j]]
		training_heatmap = get_heatmap(trad)
		Y_HEAT = [ opt_heatmap.get_cell(c.resolution, c.row, c.col).value for c in training_heatmap.sorted_cells() ]
		accumulate( Y_HEAT )
		dump_to_file( Y_HEAT, 'data/%s-sens_heat-%d.ys' % (date_series[i][-1], j) )	

# average results
Y_OPT = np.array([])
Y_HEAT = np.array([])
Y_HEAT_D = np.array([])
Y_GEOM = np.array([])

ys = [Y_OPT, Y_HEAT, Y_HEAT_D, Y_GEOM]
ys_file_names = ['data/%s-opt.ys', 'data/%s-heat.ys', 'data/%s-heatd.ys', 'data/%s-geom.ys']

for i in range( len( in_files ) ):
	for i in range(len(ys)):
		file_name = ys_file_names[i] % date_series[i][-1]
		Y_READ = np.array( read_from_file( file_name ) )
		Y = ys[i]
		# extend one or the other (or neither)
		diff = len(Y_READ) - len(Y)
		if diff > 0:
			# pad Y
			np.append(Y, np.array( [0]*diff ))
		elif diff < 0:
			# pad
			np.append(Y_READ, np.array( [0]*abs(diff) ))
		Y += Y_READ

# do the average
ys = map(lambda y: y / float(len(in_files)), ys)

print 'MAKE FIG'
X_OPT = range(1, len(Y_OPT) + 1)
X_HEAT = range(1, len(Y_HEAT) + 1)
X_HEAD_D = range(1, len(Y_HEAT_D) + 1)
X_GEOM = range(1, len(Y_GEOM) + 1)
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.set_title('Tile selection algorithms')
#ax.set_xlabel('Number of tiles cached')
#ax.set_ylabel('Cache hits')
#ax.set_xlim([0, 250000])
ax.set_ylim([0,1.1])
ax.plot(X_OPT, Y_OPT, 'r', X_HEAT, Y_HEAT, 'k--', X_HEAD_D, Y_HEAT_D, 'k', X_GEOM, Y_GEOM, 'k:')
ax.legend(('OPT', 'HEAT', 'HEAT-D', 'GEOM'),
           'lower right', shadow=True)
# change this to show...
plt.show()
#plt.savefig("graf_1.png")










