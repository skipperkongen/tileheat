from tileheat import *
from tileheat.util import *
from tileheat.analysis import *
from tileheat.optimization import *
import matplotlib.pyplot as plt

trad = CsvFileSource('../../../data/wms_wmts_twoday/wms_day1.csv') # 600K events
vald = CsvFileSource('../../../data/wms_wmts_twoday/wms_day2.csv') # 600K events

def accumulate(seq):
	for i in range(1, len(seq)):
		seq[i] += seq[i-1]

##
# OPT
##
print 'OPT'
print 'learning'
player = LogPlayer(vald)
opt = HeatmapAnalyzer( TilingScheme.by_name('kms_mod') )
player.add_analyzer( opt )
player.forward()

print 'squishing'
opt.squish()

print 'sorting'
Y_OPT = map( lambda cell: cell.value, opt.sorted_cells() )
accumulate(Y_OPT)


print 'sum = %d' % sum(Y_OPT)

print 'first 10 of %d' % len(Y_OPT)
print Y_OPT[:10]
print ''

##
# HEAT
##

print 'HEAT'
print 'learning'
player = LogPlayer(trad)	
heat = HeatmapAnalyzer( TilingScheme.by_name('kms_mod') )
player.add_analyzer( heat )
player.forward()

print 'actual'
Y_HEAT = [ opt.get_cell(c.resolution, c.row, c.col).value for c in heat.sorted_cells(exclude_zeros=False) ]
accumulate(Y_HEAT)

print 'sum = %d' % sum(Y_HEAT)

print 'first 10 of %d' % len(Y_HEAT)
print Y_HEAT[:10]
print ''

##
# HEAT-D
##

heat.dissipate(0.05,0.002)
#heat.dissipate(0.05,0.006)
#heat.dissipate(0.1,0.01)
Y_HEAT_D = [ opt.get_cell(c.resolution, c.row, c.col).value for c in heat.sorted_cells() ]
accumulate(Y_HEAT_D)

##
# GEOM
##

print 'GEOM'
print 'building'
kms = SeedingPlan.by_name('kms')
geom = TileCacheBuilder.from_seeding_plan( kms, tilesize_bytes=1 )

print 'actual'
Y_GEOM = [ opt.get_cell(c.resolution, c.row, c.col).value for c in geom.cell_generator() ]
accumulate(Y_GEOM)

print 'sum = %d' % sum(Y_GEOM)

print 'first 10 of %d' % len(Y_GEOM)
print Y_GEOM[:10]
print ''

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










