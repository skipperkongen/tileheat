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

print "HEAT-D",YS[2][1500000]
print "GEOM",YS[3][1500000]
	