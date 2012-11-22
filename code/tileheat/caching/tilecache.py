import numpy as np
from tileheat import Bbox, TilingScheme
from tileheat.heatmap import MultiscaleHeatmap

class TileCacheBuilder(object):
	"""docstring for TileCacheSelector, if no tilesize is given, use the size of this image: http://b.tile.openstreetmap.org/10/545/321.png"""
	def __init__(self):
		super(TileCacheBuilder, self).__init__()
	
	@staticmethod
	def from_heatmap_k_coverage(pop_map, k=0.99, tilesize_bytes=29*1000):
		"""docstring for get_k_percent_cache"""
		cache = TileCache(pop_map.tiling_scheme)
		# build cache
		total_heat = pop_map.total_heat()
		accumulated_hits = 0.0
		for cell in sorted( pop_map.cell_generator(exclude_zeros=True), key=lambda x: x.value, reverse=True ):
			if accumulated_hits >= k:
				break
			cache.increment_cell( cell.resolution, cell.row, cell.col, value = tilesize_bytes )
			accumulated_hits += (cell.value / total_heat)
		
		return cache
	
	@staticmethod
	def from_seeding_plan(seeding_plan, tilesize_bytes=29*1000):
		cache = TileCache(seeding_plan.tiling_scheme)
		# build cache
		for seed in seeding_plan.seeds:
			for resolution in seed.resolutions:
				cache.increment_cells_by_bbox(seed.srs, seed.bbox, resolution, tilesize_bytes)
		# make cells equal, i.e. zero or tilesize_bytes
		for level in cache.levels.values():
			matrix = level.matrix
			level.matrix = (matrix > 0).astype(int) * tilesize_bytes
		return cache
	
class TileCache(MultiscaleHeatmap):
	"""Convention is that matrix entries correspond to size of the tile that is cached. Default tile_size equals the size of this image: http://b.tile.openstreetmap.org/10/545/321.png"""
	def __init__(self, tiling_scheme):
		super(TileCache, self).__init__(tiling_scheme)
	
	def test_query(self, query):
		tiles = self.get_cells_by_bbox( query.srs, query.bbox, query.x_res )
		return CacheResult( query, np.size( tiles ), np.count_nonzero( tiles ), tiles )

	def num_tiles_in_scheme(self):
		return sum([level.num_cells() for level in self.levels.values()])
		
	def num_tiles_cached(self):
		return sum([np.count_nonzero(level.matrix) for level in self.levels.values()])
		
	def get_size_in_bytes(self):
		return self.total_heat()
	
	def boxify(self):
		pass
	
	def to_seeding_plan(self):
		pass

class CacheResult(object):
	"""docstring for CacheAnswer"""
	def __init__(self, query, num_tiles, hits, tiles):
		super(CacheResult, self).__init__()
		self.query = query
		self.num_tiles = num_tiles
		self.hits  = hits
		self.tiles = tiles

class SeedingPlan(object):
	"""docstring for SeedingPlan"""
	def __init__(self, tiling_scheme, seeds):
		super(SeedingPlan, self).__init__()
		self.tiling_scheme = tiling_scheme
		self.seeds = seeds

	@staticmethod
	def by_name(name):
		seeds = []
		if name.lower() == 'kms':
			tiling_scheme = TilingScheme.by_name( 'kms_mod' )
			resolutions = sorted(tiling_scheme.resolutions, reverse=True)
			srs = 'epsg:25832'
			# territorial omraader
			seeds.append( Seed(srs, Bbox(120000, 5600000, 1000000,6500000), resolutions[0:6]))
			# anholt
			seeds.append( Seed(srs, Bbox(653000, 6285000, 664000, 6292000), resolutions[6:12]))
			# bornholm
			seeds.append( Seed(srs, Bbox(860000, 6100000, 900000, 6150000), resolutions[6:12]))
			# nv
			seeds.append( Seed(srs, Bbox(435000, 6240000, 636000, 6410000), resolutions[6:12]))		
			# nv1
			seeds.append( Seed(srs, Bbox(550000, 6320000, 636000, 6410000), resolutions[6:12]))		
			# nv2
			seeds.append( Seed(srs, Bbox(435000, 6320000, 550000, 6410000), resolutions[6:12]))		
			# nv3
			seeds.append( Seed(srs, Bbox(435000, 6240000, 550000, 6320000), resolutions[6:12]))		
			# nv14
			seeds.append( Seed(srs, Bbox(550000, 6240000, 636000, 6410000), resolutions[6:12]))
			# nv4
			seeds.append( Seed(srs, Bbox(550000, 6240000, 636000, 6320000), resolutions[6:12]))		
			# nv23
			seeds.append( Seed(srs, Bbox(435000, 6240000, 550000, 6410000), resolutions[6:12]))		
			# sv
			seeds.append( Seed(srs, Bbox(435000, 6040000, 636000, 6240000), resolutions[6:12]))		
			# sv1
			seeds.append( Seed(srs, Bbox(435000, 6040000, 550000, 6240000), resolutions[6:12]))		
			# sv2
			seeds.append( Seed(srs, Bbox(550000, 6040000, 636000, 6240000), resolutions[6:12]))		

			# se
			seeds.append( Seed(srs, Bbox(636000, 6040000, 742000, 6240000), resolutions[6:12]))

			return SeedingPlan( tiling_scheme, seeds )

class Seed(object):
	"""docstring for Seeding"""
	def __init__(self, srs, bbox, resolutions):
		super(Seed, self).__init__()
		self.srs = srs
		self.bbox = bbox
		self.resolutions = resolutions
