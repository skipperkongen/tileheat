from tileheat import *
from tileheat.analysis import *
import numpy as np

def accumulate(seq):
	for i in range(1, len(seq)):
		seq[i] += seq[i-1]

def cummulative_distribution(matrix):
	matrix /= np.sum(matrix)
	flat = matrix.flatten()
	reindex = np.argsort(flat)[::-1]
	Y = flat[reindex]
	accumulate(Y)
	return Y

def simulate(strategies, workload, prefix=None):
	"""docstring for simulate""" 
	result = {'ys':[], 'names':[]}
	# OPT
	print "Tracking OPT"
	player = LogPlayer( workload )
	opt = HeatmapAnalyzer( TilingScheme.by_name('kms') )
	player.add_analyzer( opt )
	player.forward()
	opt.squish()
	print "Flatting OPT"
	opt_flat = opt.flatten()
	opt_reindex = np.argsort(opt_flat)[::-1]
	print "OPT, first ten: ", opt_flat[opt_reindex[:10]]
	if prefix is None:
		Y_OPT = opt_flat[opt_reindex]
	else:
		Y_OPT = opt_flat[opt_reindex[:prefix]]
	accumulate(Y_OPT)

	result['ys'].append(Y_OPT)
	result['names'].append('OPT')
 
	for strat in strategies:
		print 'Simulating',
		strat_reindex = strat.get_reindex(1)
		if prefix is None:
			Y = opt_flat[strat_reindex]
		else:
			Y = opt_flat[strat_reindex[:prefix]]
		accumulate(Y)
		result['ys'].append( Y )
		result['names'].append( strat.get_name() ) 
	return result