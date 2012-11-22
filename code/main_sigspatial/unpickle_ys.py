import cPickle as cp
import matplotlib
import matplotlib.pyplot as plt

YS = [None, None, None, None]
postf = ['_OPT.pkl','_HW-A20B10.pkl','_HWD-A20B10D10L0.pkl','_GEOM-TD.pkl']
names = ['OPT','HEAT-HW', 'HEAT-D', 'GEOM']

# sum data
for letter in 'abcdef':
	
	for i in range(4):
		file = open('stored/%s%s' % (letter, postf[i]), 'r')
		print 'Loading',file
		if YS[i] is None:                 
			YS[i] = cp.load(file)
		else:
			YS[i] += cp.load(file) 
              
# Average
for i in range(4):
	print 'Averaging', i
	YS[i] /= len('abcdef')

# Print FIG
font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Tile selection algorithms')
ax.set_xlabel('Number of tiles cached')
ax.set_ylabel('Cache hits')
ax.set_xlim([0, len(YS[0])])
ax.set_ylim([0,1.1])
for Y in YS:
	ax.plot(Y, linewidth=2)
ax.legend(tuple(names),
		   'lower right', shadow=True)
# change this to show...
plt.show()
#plt.savefig("performance.png")	 
	