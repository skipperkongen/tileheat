from tileheat import *
from tileheat.util import *
from tileheat.analysis import *
from tileheat.optimization import *

# NOTICE: Inverted order of log files
ds1 = CsvFileSource('../../../data/postfix_log2_2011_q4_rand_skrm.csv') # 45000 events
ds2 = CsvFileSource('../../../data/prefix_log2_2011_q4_rand_skrm.csv') # 45000 events

tiling_scheme = TilingScheme.by_name('kms_mod')

#################
# learn traffic #
#################
print 'Creating heatmap from first half of 2011 q4'
player = LogPlayer(ds1)
heatmap_analyzer = HeatmapAnalyzer(tiling_scheme)
player.add_analyzer( heatmap_analyzer )
player.forward()
# print heatmaps
RasterUtil.write_geotiff_heatmap(heatmap_analyzer, normalize=True, path_prefix='inv-popmap-pre-skrm')

################
# create cache #
################

print 'Creating heatmap based cache'
cache_heatmap = TileCacheBuilder.from_heatmap_k_coverage( heatmap_analyzer, k=0.9999 )
RasterUtil.write_geotiff_heatmap(cache_heatmap, normalize=True, path_prefix='inv-cache-heat-pre-skrm')

print 'Creating KMS based cache'
cache_kms = TileCacheBuilder.from_seeding_plan( SeedingPlan.by_name('kms') )
RasterUtil.write_geotiff_heatmap(cache_kms, normalize=True, path_prefix='inv-cache-kms-skrm')

##############
# test cache #
##############

print 'Testing both caches with second half of 2011 q4'

player = LogPlayer(ds2)
cache_analyzer_heatmap = CacheAnalyzer( cache_heatmap )
cache_analyzer_kms = CacheAnalyzer( cache_kms )
heatmap_analyzer = HeatmapAnalyzer(tiling_scheme)
player.add_analyzer( cache_analyzer_heatmap )
player.add_analyzer( cache_analyzer_kms )
player.add_analyzer( heatmap_analyzer )
player.forward()

RasterUtil.write_geotiff_heatmap(heatmap_analyzer, normalize=True, path_prefix='inv-popmap-post-skrm')

###############
# print stats #
###############
print ''

print 'Stats (heatmap based cache):\n'
print 'tiles total: %d' % cache_heatmap.num_tiles_in_scheme()
print 'tiles cached: %d' % cache_heatmap.num_tiles_cached()
print 'size (bytes): %d' % cache_heatmap.get_size_in_bytes()
print 'hits percentage: %.4f' % cache_analyzer_heatmap.get_hit_ratio() 
print ''

print 'Stats (kms based cache):\n'
print 'tiles total: %d' % cache_kms.num_tiles_in_scheme()
print 'tiles cached: %d' % cache_kms.num_tiles_cached()
print 'size (bytes): %d' % cache_kms.get_size_in_bytes()
print 'hits percentage: %.4f' % cache_analyzer_kms.get_hit_ratio() 
print ''

print 'Heatmap based, compared to seeding plan based:\n'
print 'size: %.1f%%' % (100 * (cache_heatmap.get_size_in_bytes() / float(cache_kms.get_size_in_bytes())))
print 'hits: %.1f%%' % (100 * (cache_analyzer_heatmap.get_hit_ratio()  / float(cache_analyzer_kms.get_hit_ratio())))

#print 'Errors: %d' % player.errors_last_run

