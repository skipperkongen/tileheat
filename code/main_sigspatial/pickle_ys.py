from tileheat.predict import *
from tileheat import *
import cPickle
import matplotlib.pyplot as plt
import gc

datasets = [
#	(['fast/ufast1.csv', 'fast/ufast2.csv'], 'fast/ufast3.csv'),
#	(['fast/fast1.csv', 'fast/fast2.csv'], 'fast/fast3.csv'),
	(['tileheat_dump/a_1.csv', 'tileheat_dump/a_2.csv', 'tileheat_dump/a_3.csv'], 'tileheat_dump/a_4.csv'),
	(['tileheat_dump/b_1.csv', 'tileheat_dump/b_2.csv', 'tileheat_dump/b_3.csv'], 'tileheat_dump/b_4.csv'),		 
	(['tileheat_dump/c_1.csv', 'tileheat_dump/c_2.csv', 'tileheat_dump/c_3.csv'], 'tileheat_dump/c_4.csv'),
	(['tileheat_dump/d_1.csv', 'tileheat_dump/d_2.csv', 'tileheat_dump/d_3.csv'], 'tileheat_dump/d_4.csv'),
	(['tileheat_dump/e_1.csv', 'tileheat_dump/e_2.csv', 'tileheat_dump/e_3.csv'], 'tileheat_dump/e_4.csv'),
	(['tileheat_dump/f_1.csv', 'tileheat_dump/f_2.csv', 'tileheat_dump/f_3.csv'], 'tileheat_dump/f_4.csv')
]						 

prefix = '../../../data/'

alpha = 0.2
beta = 0.1
dist = 10
loss = 0.002  # mu

def train(algorithm, filenames):
	for f in filenames:	 
		print "Training", algorithm.get_name(), "with", f
		ds = CsvFileSource("%s%s" % (prefix, f), event_type='WMS')
		algorithm.train(ds)	

def validate(algorithms, filename):
	print "Validating with", filename
	vald = "%s%s" % (prefix, filename)
	return simulate(algorithms, CsvFileSource( vald, event_type='WMS' ), prefix=None)


print "Testing alpha: %.2f	beta: %.2f " % (alpha, beta)
for tup in datasets:

	hw = HoltWinter( TilingScheme.by_name('kms'), alpha, beta)
	hwd = HoltWinterDissipate( TilingScheme.by_name('kms'), alpha, beta, dist, loss)
	geom = Geom( SeedingPlan.by_name('kms') )
	geomtd = TopDownGeom (SeedingPlan.by_name('kms') )
	# train
	train(hw, tup[0])
	train(hwd, tup[0])
	# validate
	sim_result = validate([hw, hwd, geom, geomtd], tup[1])
	#sim_result = validate([hw, geom, geomtd], tup[1])

	# save series
	ys = sim_result['ys']
	names = sim_result['names']
	
	print "Pickleing"
	for pair in zip(ys,names):
		fn = "%s_%s.pkl" % (tup[1][-7:-6], pair[1])
		output = open(fn, 'wb')
		cPickle.dump(pair[0], output)
		output.close()

	print 'MAKE FIG'
	ar = (1.61803399*2, 1)
	factor = 4
	dpi=10

	
	fig = plt.figure(figsize=(ar[0]*factor, ar[1]*factor))
	ax = fig.add_subplot(111)
	ax.set_title('Tile selection algorithms')
	ax.set_xlabel('Number of tiles cached')
	ax.set_ylabel('Cache hits')
	ax.set_xlim([0, len(sim_result['ys'][0])])
	ax.set_ylim([0,1.1])
	for Y in sim_result['ys']:
		ax.plot(Y)
	ax.legend(tuple(sim_result['names']),
			   'lower right', shadow=True)
	# change this to show...
	#plt.show()
	plt.savefig("performance.png")	 
	